import asyncio
import json
import http.cookies

from urllib.parse import urlsplit, parse_qsl

from aiohttp.multidict import MultiDict, MutableMultiDict

from .errors import JsonLoadError, JsonDecodeError


__all__ = [
    'Request',
    'Response',
    ]


class Response:

    def __init__(self):
        self.headers = MutableMultiDict()
        self._cookies = http.cookies.SimpleCookie()
        self._deleted_cookies = set()

    def _copy_cookies(self):
        for cookie in self._cookies.values():
            value = cookie.output(header='')[1:]
            self.headers.add('Set-Cookie', value)

    @property
    def cookies(self):
        return self._cookies

    def set_cookie(self, name, value, *, expires=None,
                   domain=None, max_age=None, path=None,
                   secure=None, httponly=None, version=None):
        """Set or update response cookie.

        Sets new cookie or updates existent with new value.
        Also updates only those params which are not None.
        """
        if name in self._deleted_cookies:
            self._deleted_cookies.remove(name)
            self._cookies.pop(name, None)

        self._cookies[name] = value
        c = self._cookies[name]
        if expires is not None:
            c['expires'] = expires
        if domain is not None:
            c['domain'] = domain
        if max_age is not None:
            c['max-age'] = max_age
        if path is not None:
            c['path'] = path
        if secure is not None:
            c['secure'] = secure
        if httponly is not None:
            c['httponly'] = httponly
        if version is not None:
            c['version'] = version

    def del_cookie(self, name, *, domain=None, path=None):
        """Delete cookie.

        Creates new empty expired cookie.
        """
        # TODO: do we need domain/path here?
        self._cookies.pop(name, None)
        self.set_cookie(name, '', max_age=0, domain=domain, path=path)
        self._deleted_cookies.add(name)


class Request:

    def __init__(self, host, message, req_body, *,
                 session_factory=None, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        res = urlsplit(message.path)
        self._loop = loop
        self.version = message.version
        self.method = message.method.upper()
        self.host = message.headers.get('HOST', host)
        self.host_url = 'http://' + self.host
        self.path_qs = message.path
        self.path = res.path
        self.path_url = self.host_url + self.path
        self.url = self.host_url + self.path_qs
        self.query_string = res.query
        self.args = MultiDict(parse_qsl(res.query))
        self.headers = message.headers
        self.matchdict = {}
        self._request_body = req_body
        self._response = Response()
        self._session_factory = session_factory
        self._session_fut = None
        self._json_body = None
        self._cookies = None
        self._on_response = []

    @property
    def response(self):
        """Response object."""
        return self._response

    @property
    def session(self):
        if self._session_fut is None:
            self._session_fut = fut = asyncio.Future(loop=self._loop)
            if self._session_factory is not None:
                self._session_factory(self, fut)
            else:
                fut.set_result(None)
        return self._session_fut

    @property
    def json_body(self):
        if self._json_body is None:
            if self._request_body:
                # TODO: store generated exception and
                # don't try to parse json next time
                try:
                    decoded = self._request_body.decode('utf-8')
                except UnicodeDecodeError as exc:
                    raise JsonDecodeError(exc.encoding,
                                          exc.object,
                                          exc.start,
                                          exc.end,
                                          "Json body is not utf-8 encoded",
                                          )
                else:
                    try:
                        self._json_body = json.loads(decoded)
                    except (ValueError):
                        raise JsonLoadError("Json body cannot be decoded",
                                            decoded)
            else:
                raise JsonLoadError("Request hasn't a body")
        return self._json_body

    @property
    def cookies(self):
        """Return request cookies.

        A read-only dictionary-like object.
        """
        if self._cookies is None:
            raw = self.headers.get('COOKIE', '')
            parsed = http.cookies.SimpleCookie(raw)
            self._cookies = MultiDict({key: val.value
                                       for key, val in parsed.items()})
        return self._cookies

    def add_response_callback(self, callback, *args, **kwargs):
        """Add callback to be trigger when request is ready to be sent.
        """
        self._on_response.append((callback, args, kwargs))

    @asyncio.coroutine
    def _call_response_callbacks(self):
        callbacks = self._on_response[:]
        for callback, args, kwargs in callbacks:
            if asyncio.iscoroutinefunction(callback):
                yield from callback(self, *args, **kwargs)
            else:
                callback(self, *args, **kwargs)
        self.response._copy_cookies()
