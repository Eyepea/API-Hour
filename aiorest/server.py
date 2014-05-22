import asyncio
import collections
import inspect
import json
import re
import aiohttp

from types import MethodType

from . import errors
from .handler import RESTRequestHandler


__all__ = [
    'RESTServer',
    ]


Entry = collections.namedtuple('Entry', 'regex method handler use_request'
                                        ' check_cors cors_options')


class RESTServer:

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
                 enable_cors=False, loop=None, **kwargs):
        assert session_factory is None or callable(session_factory), \
            "session_factory must be None or callable (coroutine) function"
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        super().__init__()
        self.hostname = hostname
        self.session_factory = session_factory
        self._enable_cors = enable_cors
        self._kwargs = kwargs
        self._urls = []

    def make_handler(self):
        return RESTRequestHandler(self, hostname=self.hostname,
                                  session_factory=self.session_factory,
                                  loop=self._loop,
                                  **self._kwargs)

    @property
    def cors_enabled(self):
        return self._enable_cors

    def add_url(self, method, path, handler, use_request=False,
                check_cors=True, cors_options={}):
        """XXX"""
        assert callable(handler), handler
        assert not set(cors_options) - set(self.CORS_OPTIONS), \
            'Got bad CORS options: {}'.format(
                set(cors_options) - set(self.CORS_OPTIONS))
        if isinstance(handler, MethodType):
            holder = handler.__func__
        else:
            holder = handler
        sig = holder.__signature__ = inspect.signature(holder)

        if use_request:
            if use_request is True:
                use_request = 'request'
            try:
                p = sig.parameters[use_request]
            except KeyError:
                raise TypeError('handler {!r} has no argument {}'
                                .format(handler, use_request))
            assert p.annotation is p.empty, ("handler's arg {} "
                                             "for request name "
                                             "should not have "
                                             "annotation").format(use_request)
        else:
            use_request = None
        assert path.startswith('/')
        assert callable(handler), handler
        method = method.upper()
        assert method in self.METHODS, method
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
        self._urls.append(Entry(compiled, method, handler, use_request,
                                check_cors, cors_options))

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
        sig = inspect.signature(handler)
        kwargs = match.groupdict()
        if entry.use_request:
            assert entry.use_request not in kwargs, (entry.use_request, kwargs)
            kwargs[entry.use_request] = request
        try:
            args, kwargs, ret_ann = self.construct_args(sig, kwargs)
            if asyncio.iscoroutinefunction(handler):
                ret = yield from handler(*args, **kwargs)
            else:
                ret = handler(*args, **kwargs)
            if ret_ann is not None:
                ret = ret_ann(ret)
        except aiohttp.HttpException as exc:
            raise
        except Exception as exc:
            # add log about error
            raise aiohttp.HttpErrorException(500,
                                             "Internal Server Error") from exc
        else:
            return json.dumps(ret)

    def construct_args(self, sig, kwargs):
        try:
            bargs = sig.bind(**kwargs)
        except TypeError:
            raise
        else:
            args = bargs.arguments
            marker = object()
            for name, param in sig.parameters.items():
                if param.annotation is param.empty:
                    continue
                val = args.get(name, marker)
                if val is marker:
                    continue    # Skip default value
                try:
                    args[name] = param.annotation(val)
                except (TypeError, ValueError) as exc:
                    raise ValueError(
                        'Invalid value for argument {!r}: {!r}'
                        .format(name, exc)) from exc
            if sig.return_annotation is not sig.empty:
                return bargs.args, bargs.kwargs, sig.return_annotation
            return bargs.args, bargs.kwargs, None

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
