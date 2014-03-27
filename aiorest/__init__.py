import collections
import email
import functools
import inspect
import json
import re
import time

import asyncio
import aiohttp, aiohttp.server

from types import MethodType


Entry = collections.namedtuple('Entry', 'regex method handler')


class Request:

    def __init__(self, message, headers):
        self._message = message
        self.version = message.version
        self.method = message.method
        self.path = message.path
        self.headers = headers

    @classmethod
    def construct(cls, message, headers, payload, response):
        return cls(message, payload)


class Response:

    def __init__(self, response_impl):
        self._impl = response_impl

    @classmethod
    def construct(cls, message, headers, payload, response):
        return cls(response)


class PostJson:

    def __init__(self, payload):
        self._payload = payload

    @classmethod
    def construct(cls, message, headers, payload, response):
        return cls(payload)


class RESTServer(aiohttp.server.ServerHttpProtocol):

    DYN = re.compile(r'^\{.+\}$')
    PLAIN = re.compile(r'^[^{}]+$')

    METHODS = {'POST', 'GET', 'PUT', 'DELETE', 'PATCH', 'HEAD'}

    def __init__(self, *, hostname, **kwargs):
        super().__init__(**kwargs)
        self.hostname = hostname
        self._urls = []
        self._default_anns = {Request: Request.construct,
                              Response: Response.construct,
                              PostJson: PostJson.construct}

    @asyncio.coroutine
    def handle_request(self, message, payload):
        now = time.time()
        #self.log.debug("Start handle request %r at %d", message, now)

        try:
            headers = email.message.Message()
            for hdr, val in message.headers:
                headers.add_header(hdr, val)

            response = aiohttp.Response(self.transport, 200)
            body = yield from self.dispatch(message, headers, payload, response)
            bbody = body.encode('utf-8')

            response.add_header('Host', self.hostname)
            response.add_header('Content-Type', 'application/json')
            response.add_header('Content-Length', str(len(bbody)))

            # content encoding
            accept_encoding = headers.get('accept-encoding', '').lower()
            ## if 'deflate' in accept_encoding:
            ##     response.add_header('Transfer-Encoding', 'chunked')
            ##     response.add_header('Content-Encoding', 'deflate')
            ##     response.add_compression_filter('deflate')
            ## elif 'gzip' in accept_encoding:
            ##     response.add_header('Transfer-Encoding', 'chunked')
            ##     response.add_header('Content-Encoding', 'gzip')
            ##     response.add_compression_filter('gzip')
            ## else:
            ##     response.add_header('Content-Length', str(len(bbody)))

            response.send_headers()
            response.write(bbody)
            response.write_eof()
            if response.keep_alive():
                self.keep_alive(True)

            #self.log.debug("Fihish handle request %r at %d -> %s",
            #               message, time.time(), body)
            self.log_access(message, None, response, time.time() - now)
        except Exception as exc:
            #self.log.exception("Cannot handle request %r", message)
            raise

    def add_url(self, method, path, handler, anns=()):
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
                raise ValueError("Invalid path '{}'['{}']".format(path, part))
        pattern = '/' + '/'.join(regexp)
        if path.endswith('/') and pattern != '/':
            pattern += '/'
        try:
            compiled = re.compile('^' + pattern + '$')
        except re.error:
            raise ValueError("Invalid path '{}'".format(path))
        if isinstance(handler, MethodType):
            holder = handler.__func__
        else:
            holder = handler
        holder.__signature__ = inspect.signature(handler)
        self._urls.append(Entry(compiled, method, handler))

    @asyncio.coroutine
    def dispatch(self, message, headers, payload, response):
        path = message.path
        method = message.method.upper()
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
        sig = inspect.signature(handler)
        try:
            args, kwargs, ret_ann = self.construct_args(sig, message, headers,
                                                        payload, response,
                                                        match.groupdict())
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

    def construct_args(self, sig, message, headers, payload, response, kwargs):
        # add signature check
        extra = set()
        for name, param in sig.parameters.items():
            if param.annotation is param.empty:
                continue
            ctor = self._default_anns.get(param.annotation)
            if ctor is not None:
                assert param.default is param.empty, param
                assert name not in kwargs, (kwargs, name)
                extra.add(name)
                kwargs[name] = ctor(message, headers, payload, response)
        try:
            bargs = sig.bind(**kwargs)
        except TypeError:
            raise
        else:
            args = bargs.arguments
            for name, param in sig.parameters.items():
                if name in extra:
                    continue
                if param.annotation is param.empty:
                    continue
                val = args.get(name, param.default)
                # NOTE: default value always being passed through annotation
                #       is it realy neccessary?
                try:
                    args[name] = param.annotation(val)
                except (TypeError, ValueError) as exc:
                    raise ParametersError(
                        'Invalid value for argument {!r}: {!r}'
                        .format(name, exc)) from exc
            if sig.return_annotation is not sig.empty:
                return bargs.args, bargs.kwargs, sig.return_annotation
            return bargs.args, bargs.kwargs, None
