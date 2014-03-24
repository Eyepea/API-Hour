import collections
import functools
import inspect
import json
import re

import asyncio
import aiohttp, aiohttp.server

from types import MethodType


Entry = collections.namedtuple('Entry', 'regex method handler')


class RESTServer(aiohttp.server.ServerHttpProtocol):

    DYN = re.compile(r'^\{.+\}$')
    PLAIN = re.compile(r'^[^{}]+$')

    METHODS = {'POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'HEAD'}

    def __init__(self, *, hostname, **kwargs):
        super().__init__(**kwargs)
        self.hostname = hostname
        self._urls = []

    @asyncio.coroutine
    def handle_request(self, message, payload):
        method = message.method
        path = message.path
        version = message.version

        headers = email.message.Message()
        for hdr, val in message.headers:
            headers.add_header(hdr, val)

        response = aiohttp.Response(self.transport, 200)
        body = yield from self.dispatch(method, path, message, payload)
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

    def add_url(self, method, path, handler):
        assert path.startswith('/')
        assert callable(handler), handler
        method = method.upper()
        assert method in self.METHODS, method
        regexp = []
        for part in path.split('/'):
            if not part:
                continue
            if self.DYN.match(part):
                regexp.append('(?P<'+part[1:-1]+'>.+)')
            elif self.PLAIN.match(part):
                regexp.append(part)
            else:
                raise RuntimeError("Invalid part '{}'['{}']".format(part, path))
        pattern = '/' + '/'.join(regexp)
        if path.endswith('/') and pattern != '/':
            pattern += '/'
        compiled = re.compile(pattern)
        if isinstance(handler, MethodType):
            holder = handler.__func__
        else:
            holder = handler
        holder.__signature__ = inspect.signature(handler)
        self._urls.append(Entry(compiled, method, handler))

    @asyncio.coroutine
    def dispatch(self, method, path, message, payload):
        allowed_methods = set()
        for entry in self._urls:
            match = entry.regex.match(path)
            if match is None:
                continue
            if entry.method != method:
                allowed_methods.add(entry.method)
            else:
                break
        else:
            if allowed_methods:
                allow = ', '.join(sorted(allowed_methods))
                # add log
                raise aiohttp.HttpErrorException(405,
                                                 headers=(('Allow', allow),))
            else:
                # add log
                raise aiohttp.HttpErrorException(404, "Not Found")

        handler = entry.handler
        signature = inspect.signature(handler)
        # add signature check
        args, kwargs = self.construct_args(signature, match.groupdict())
        try:
            if asyncio.iscoroutinefunction(handler):
                ret = yield from handler(*args, **kwargs)
            else:
                ret = handler(*args, **kwargs)
        except aiohttp.HttpException as exc:
            raise
        except Exception as exc:
            # add log about error
            raise aiohttp.HttpErrorException(500, "Internal Server Error")
        else:
            return json.dumps(ret)

    def construct_args(self, signature, variables):
        return (), variables
