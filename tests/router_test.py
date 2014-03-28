import unittest
from unittest import mock

import asyncio
import aiohttp
import email
from aiorest import RESTServer, Request
import json


class RouterTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.server = RESTServer(hostname='example.com', loop=self.loop)

    def tearDown(self):
        self.loop.close()

    def test_add_url(self):
        handler = lambda id: None
        self.server.add_url('post', '/post/{id}', handler)
        self.assertEqual(1, len(self.server._urls))
        entry = self.server._urls[0]
        self.assertEqual('POST', entry.method)
        self.assertIs(handler, entry.handler)
        self.assertEqual('^/post/(?P<id>.+)$', entry.regex.pattern)

    def test_add_url_invalid1(self):
        with self.assertRaises(ValueError):
            self.server.add_url('post', '/post/{id', lambda:None)

    def test_add_url_invalid2(self):
        with self.assertRaises(ValueError):
            self.server.add_url('post', '/post/{id{}}', lambda:None)

    def test_add_url_invalid3(self):
        with self.assertRaises(ValueError):
            self.server.add_url('post', '/post/{id{}', lambda:None)

    def test_add_url_invalid4(self):
        with self.assertRaises(ValueError):
            self.server.add_url('post', '/post/{id"}', lambda:None)

    def test_add_url_invalid5(self):
        with self.assertRaises(ValueError):
            self.server.add_url('post', '/post"{id}', lambda:None)

    def test_dispatch_not_found(self):
        m = mock.Mock()
        self.server.add_url('post', '/post/{id}', m)
        self.server.add_url('get', '/post/{id}', m)

        @asyncio.coroutine
        def go():
            with self.assertRaises(aiohttp.HttpException) as ctx:
                request = Request('host', aiohttp.RawRequestMessage(
                    'POST', '/not/found', '1.1', (), True, None),
                    email.message.Message(), None)
                yield from self.server.dispatch(request)
            self.assertEqual(404, ctx.exception.code)

        self.assertFalse(m.called)
        self.loop.run_until_complete(go())

    def test_dispatch_method_not_allowed(self):
        m = mock.Mock()
        self.server.add_url('post', '/post/{id}', m)
        self.server.add_url('get', '/post/{id}', m)

        @asyncio.coroutine
        def go():
            with self.assertRaises(aiohttp.HttpException) as ctx:
                request = Request('host',
                    aiohttp.RawRequestMessage('DELETE', '/post/123', '1.1',
                                              (), True, None),
                    email.message.Message(), None)
                yield from self.server.dispatch(request)
            self.assertEqual(405, ctx.exception.code)
            self.assertEqual((('Allow', 'GET, POST'),), ctx.exception.headers)

        self.assertFalse(m.called)
        self.loop.run_until_complete(go())

    def test_dispatch(self):
        def f(id):
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)
        ret = self.loop.run_until_complete(self.server.dispatch(request))
        # json.loads is required to avoid items order in dict
        self.assertEqual({"b": 2, "a": 1}, json.loads(ret))

    def test_dispatch_with_ending_slash(self):
        def f(id):
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}/', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123/', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)
        ret = self.loop.run_until_complete(self.server.dispatch(request))
        # json.loads is required to avoid items order in dict
        self.assertEqual({"b": 2, "a": 1}, json.loads(ret))

    def test_dispatch_with_ending_slash_not_found1(self):
        def f(id):
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}/', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        with self.assertRaises(aiohttp.HttpException) as ctx:
            self.loop.run_until_complete(self.server.dispatch(request))
        self.assertEqual(404, ctx.exception.code)

    def test_dispatch_with_ending_slash_not_found2(self):
        def f(id):
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}/', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/po/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        with self.assertRaises(aiohttp.HttpException) as ctx:
            self.loop.run_until_complete(self.server.dispatch(request))
        self.assertEqual(404, ctx.exception.code)

    def test_dispatch_bad_signature(self):
        def f():
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        @asyncio.coroutine
        def go():
            with self.assertRaises(aiohttp.HttpException) as ctx:
                yield from self.server.dispatch(request)
            self.assertEqual(500, ctx.exception.code)

        self.loop.run_until_complete(go())

    def test_dispatch_bad_signature2(self):
        def f(unknown_argname):
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        @asyncio.coroutine
        def go():
            with self.assertRaises(aiohttp.HttpException) as ctx:
                yield from self.server.dispatch(request)
            self.assertEqual(500, ctx.exception.code)

        self.loop.run_until_complete(go())

    def test_dispatch_http_exception_from_handler(self):
        def f(id):
            raise aiohttp.HttpErrorException(
                401,
                headers=(('WWW-Authenticate', 'Basic'),))
        self.server.add_url('get', '/post/{id}', f)

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        @asyncio.coroutine
        def go():
            with self.assertRaises(aiohttp.HttpException) as ctx:
                yield from self.server.dispatch(request)
            self.assertEqual(401, ctx.exception.code)
            self.assertEqual((('WWW-Authenticate', 'Basic'),),
                             ctx.exception.headers)

        self.loop.run_until_complete(go())

    def test_dispatch_with_request(self):
        def f(id, req):
            self.assertIsInstance(req, Request)
            self.assertEqual('GET', req.method)
            self.assertEqual('/post/123', req.path)
            return {'a': 1, 'b': 2}
        self.server.add_url('get', '/post/{id}', f, use_request='req')

        request = Request('host',
            aiohttp.RawRequestMessage('GET', '/post/123', '1.1',
                                      (), True, None),
                                      email.message.Message(), None)

        ret = self.loop.run_until_complete(self.server.dispatch(request))
        # json.loads is required to avoid items order in dict
        self.assertEqual({"b": 2, "a": 1}, json.loads(ret))
