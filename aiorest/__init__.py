import functools
import asyncio
import aiohttp, aiohttp.server


class rest:
    def __init__(self, method, name=None):
        self.method = method
        self.name = name

    def __call__(self, func):
        if self.name is None:
            self.name = func.__name__
        @functools.wraps(func)
        def wrapped(self, *args, **kwargs):
            return func(self, *args, **kwargs)
        return wrapped



class Resource:
    def __init__(self):
        self._apis = {}
        for name in dir(self.__class__):
            val = getattr(self.__class__.name)
            if isinstance(val, rest):
                self._apis[(val.name, val.method)] = val

    def dispatch(self, message):
        try:
            resource = self._apis[request.path]
            try:
                method = resource[message.method]
                method(self)
            except KeyError:
                allow = ', '.join(resource)
                raise aiohttp.HttpErrorException(405,
                                                 headers=(('Allow', allow)))
        except KeyError:
            raise aiohttp.HttpErrorException(404)


class RESTServer(aiohttp.server.ServerHttpProtocol):
    def __init__(self, *, hostname, **kwargs):
        super().__init__(**kwargs)
        self.hostname = hostname

    @asyncio.coroutine
    def handle_request(self, message, payload):
        method = message.method
        path = message.path
        version = message.version

        headers = email.message.Message()
        for hdr, val in message.headers:
            print(hdr, val)
            headers.add_header(hdr, val)

        response = aiohttp.Response(self.transport, 200)
        body = yield from self.dispatch(method, path, messaage, payload)
        response.add_header('Content-Length', len(body))
        response.add_header('Host', self.hostname)
        response.add_header('Content-Type', 'application/json')
        response.add_header('Server', 'asyncio/aiorest')

        # content encoding
        accept_encoding = headers.get('accept-encoding', '').lower()
        if 'deflate' in accept_encoding:
            response.add_header('Content-Encoding', 'deflate')
            response.add_compression_filter('deflate')
        elif 'gzip' in accept_encoding:
            response.add_header('Content-Encoding', 'gzip')
            response.add_compression_filter('gzip')

        response.send_headers()
        response.write(body.encode('utf-8'))
        response.write_eof()
        if response.keep_alive():
            self.keep_alive(True)

        self.log_access(message, None, response, time.time() - now)
