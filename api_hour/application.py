import asyncio
import collections
import inspect
import re
import logging

import aiohttp
from . import errors
from .handler import RESTRequestHandler
from .security import AbstractIdentityPolicy, AbstractAuthorizationPolicy
from . import serialize


__all__ = [
    'Application',
    ]

LOG = logging.getLogger(__name__)

Entry = collections.namedtuple('Entry', 'regex method handler'
                                        ' check_cors cors_options')


class Application:

    DYN = re.compile(r'^\{[_a-zA-Z][_a-zA-Z0-9]*\}$')
    GOOD = r'[^{}/]+'
    PLAIN = re.compile('^'+GOOD+'$')

    METHODS = {'POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'HEAD'}

    CORS_OPTIONS = {
        'allow-origin': '*',
        'allow-credentials': False,
        'allow-headers': None,
        'expose-headers': None,
        'max-age': 86400,
    }

    def __init__(self, *, hostname, session_factory=None,
                 enable_cors=False, loop=None,
                 identity_policy=None, auth_policy=None, config=None, **kwargs):
        assert session_factory is None or callable(session_factory), \
            "session_factory must be None or callable (coroutine) function"
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        super().__init__()
        self.hostname = hostname
        self.session_factory = session_factory
        self._enable_cors = enable_cors
        self._identity_policy = identity_policy
        if identity_policy:
            assert isinstance(identity_policy, AbstractIdentityPolicy)
        self._auth_policy = auth_policy
        if auth_policy:
            assert isinstance(auth_policy, AbstractAuthorizationPolicy)
        self.config = config
        self._kwargs = kwargs
        self._urls = []

    def make_handler(self):
        return RESTRequestHandler(self, hostname=self.hostname,
                                  session_factory=self.session_factory,
                                  loop=self._loop,
                                  identity_policy=self._identity_policy,
                                  auth_policy=self._auth_policy,
                                  **self._kwargs)

    @property
    def cors_enabled(self):
        return self._enable_cors

    def add_url(self, method, path, handler,
                check_cors=True, cors_options={}):
        """XXX"""
        assert callable(handler), handler
        assert not set(cors_options) - set(self.CORS_OPTIONS), \
            'Got bad CORS options: {}'.format(
                set(cors_options) - set(self.CORS_OPTIONS))

        assert path.startswith('/')
        assert callable(handler), handler
        regexp = []
        for part in path.split('/'):
            if not part:
                continue
            if self.DYN.match(part):
                regexp.append('(?P<'+part[1:-1]+'>'+self.GOOD+')')
            elif self.PLAIN.match(part):
                regexp.append(part)
            else:
                raise ValueError("Invalid path '{}'['{}']".format(path, part))
        pattern = '/' + '/'.join(regexp)
        if path.endswith('/') and pattern != '/':
            pattern += '/'
        try:
            compiled = re.compile('^' + pattern + '$')
        except re.error:
            raise ValueError("Invalid path '{}'".format(path))
        cors_options = collections.ChainMap(cors_options, self.CORS_OPTIONS)
        allow_origin = cors_options.get('allow-origin')
        if allow_origin is not None:
            assert callable(allow_origin) \
                or isinstance(allow_origin, (collections.Sequence, str)), \
                "Invalid 'allow-origin' option {!r}".format(allow_origin)

        if isinstance(method, str):
            method = [method]

        if hasattr(method, '__iter__'):
            for http_verb in method:
                http_verb = http_verb.upper()
                assert http_verb in self.METHODS, http_verb
                self._urls.append(Entry(compiled, http_verb, handler,
                                        check_cors, cors_options))
        else:
            raise ValueError("The HTTP verb must be a String or Iterable")

    @asyncio.coroutine
    def dispatch(self, request):
        path = request.path
        method = request.method
        allowed_methods = set()
        check_cors = False
        if method == 'OPTIONS' and self.cors_enabled:
            check_cors = True
            method = request.headers.get('ACCESS-CONTROL-REQUEST-METHOD')
            if not method:
                raise errors.RESTError(404, "Not Found")
        for entry in self._urls:
            match = entry.regex.match(path)
            if match is None:
                continue
            if entry.method != method:
                allowed_methods.add(entry.method)
            elif check_cors and entry.check_cors:
                headers = tuple(self._make_cors_headers(request,
                                                        entry.cors_options))
                raise errors.HttpCorsOptions(headers)
            else:
                break
        else:
            if allowed_methods:
                allow = ', '.join(sorted(allowed_methods))
                # add log
                raise errors.RESTError(405, "Not Allowed",
                                       json_body={'allowed_methods': allow},
                                       headers=(('Allow', allow),))
            else:
                # add log
                raise errors.RESTError(404, "Not Found")
        if self.cors_enabled and entry.check_cors:
            headers = tuple(self._make_cors_headers(request,
                                                    entry.cors_options))
            request.response.headers.extend(headers)

        handler = entry.handler
        request.matchdict = match.groupdict()

        sig = inspect.signature(handler)
        ret_ann = None
        if sig.return_annotation is not sig.empty:
            ret_ann = sig.return_annotation
        try:
            if asyncio.iscoroutinefunction(handler):
                ret = yield from handler(request)
            else:
                ret = handler(request)
            if ret_ann is not None:
                ret = ret_ann(ret)
        except errors.JsonDecodeError as exc:
            raise errors.RESTError(400, exc.reason)
        except errors.JsonLoadError as exc:
            raise errors.RESTError(400, exc.args[0])
        except aiohttp.HttpException as exc:
            raise
        except Exception as exc:
            # add log about error
            raise aiohttp.HttpErrorException(500,
                                             "Internal Server Error") from exc
        else:
            if isinstance(ret, serialize.Base):
                return ret.serialize(request)
            else:
                return serialize.Json(ret).serialize(request)

    def _make_cors_headers(self, request, cors_options):
        option = cors_options.get
        header = request.headers.get

        # TODO: implement real CORS check
        origin = header('ORIGIN')
        allow_origin = option('allow-origin')
        method = header('ACCESS-CONTROL-REQUEST-METHOD')

        # check bad request cases
        if origin is None or origin == '*' or not allow_origin:
            return
        if request.method == 'OPTIONS' and not method:
            return

        allow_creds = option('allow-credentials')
        if callable(allow_origin):
            allow_origin = allow_origin(request, cors_options)
        if isinstance(allow_origin, str):
            allow_origin = (allow_origin,)
        if '*' in allow_origin:
            if allow_creds:
                yield ('Access-Control-Allow-Origin', origin)
            else:
                yield ('Access-Control-Allow-Origin', '*')
        elif origin in allow_origin:
            yield ('Access-Control-Allow-Origin', origin)

        if method:
            yield ('Access-Control-Allow-Methods', method)

        allow_headers = option('allow-headers')
        if allow_headers:
            assert isinstance(allow_headers, (str, collections.Sequence))
            if not isinstance(allow_headers, str):
                allow_headers = ', '.join(allow_headers)
            yield ('Access-Control-Allow-Headers', allow_headers)
        if allow_creds:
            yield ('Access-Control-Allow-Credentials', allow_creds and 'true')

    @asyncio.coroutine
    def start(self):
        raise NotImplementedError("Please Implement this method")

    def stop(self):
        raise NotImplementedError("Please Implement this method")