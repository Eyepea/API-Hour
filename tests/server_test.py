import unittest

import asyncio
import aiohttp
from aiorest import RESTServer
import json

from test.support import find_unused_port


class REST:
    def __init__(self, case):
        self.case = case

    def func_POST(self, id, request):
        self.case.assertEqual('123', id)
        self.case.assertEqual({'q': 'val'}, request.json_body)
        return {'success': True}

    def func_GET(self, id: int, req):
        self.case.assertEqual(123, id)
        with self.case.assertRaises(ValueError):
            req.json_body
        return {'success': True}

    def func_GET2(self, id: int, req):
        self.case.assertEqual(123, id)
        with self.case.assertRaises(ValueError):
            req.json_body
        self.case.assertEqual((1, 1), req.version)
        self.case.assertEqual('GET', req.method)
        self.case.assertEqual('localhost', req.host)
        self.case.assertEqual('http://localhost', req.host_url)
        self.case.assertEqual('/post/123/2?a=1&b=2', req.path_qs)
        self.case.assertEqual('/post/123/2', req.path)
        self.case.assertEqual('http://localhost/post/123/2', req.path_url)
        self.case.assertEqual('http://localhost/post/123/2?a=1&b=2', req.url)
        self.case.assertEqual('a=1&b=2', req.query_string)
        self.case.assertEqual('1', req.args['a'])
        self.case.assertEqual('2', req.args['b'])
        return {'success': True, 'args': list(req.args)}

    @asyncio.coroutine
    def coro_set_cookie(self, value:int, req):
        response = yield from req.response
        response.set_cookie('test_cookie', value)
        return {'success': True}

    def func_get_cookie(self, req):
        return {'success': True,
                'cookie': req.cookies['test_cookie']}


class RouterTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.server = RESTServer(debug=True, keep_alive=75,
                                 hostname='localhost', loop=self.loop)
        rest = REST(self)
        self.server.add_url('POST', '/post/{id}', rest.func_POST,
                            use_request=True)
        self.server.add_url('GET', '/post/{id}', rest.func_GET,
                            use_request='req')
        self.server.add_url('GET', '/post/{id}/2', rest.func_GET2,
                            use_request='req')
        self.server.add_url('GET', '/cookie/{value}', rest.coro_set_cookie,
                            use_request='req')
        self.server.add_url('GET', '/get_cookie/', rest.func_get_cookie,
                            use_request='req')

    def tearDown(self):
        self.loop.close()

    def test_simple_POST(self):
        port = find_unused_port()

        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/post/123'.format(port)

        def query():
            response = yield from aiohttp.request(
                'POST', url,
                data=json.dumps({'q': 'val'}).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                loop=self.loop)
            self.assertEqual(200, response.status)
            data = yield from response.read()
            self.assertEqual(b'{"success": true}', data)

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_simple_GET(self):
        port = find_unused_port()

        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/post/123'.format(port)

        def query():
            response = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, response.status)
            data = yield from response.read()
            self.assertEqual(b'{"success": true}', data)

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_GET_with_query_string(self):
        port = find_unused_port()

        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/post/123/2?a=1&b=2'.format(port)

        def query():
            response = yield from aiohttp.request('GET', url, loop=self.loop)
            self.assertEqual(200, response.status)
            data = yield from response.read()
            dct = json.loads(data.decode('utf-8'))
            self.assertEqual({'success': True,
                              'args': ['a', 'b'],
                              }, dct)

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_set_cookie(self):
        port = find_unused_port()

        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/cookie/123'.format(port)

        @asyncio.coroutine
        def query():
            response = yield from aiohttp.request('GET', url, loop=self.loop)
            yield from response.read_and_close()
            self.assertEqual(200, response.status)
            self.assertIn('test_cookie', response.cookies)
            self.assertEqual(response.cookies['test_cookie'].value, '123')

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_get_cookie(self):
        port = find_unused_port()

        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/get_cookie/'.format(port)

        @asyncio.coroutine
        def query():
            response = yield from aiohttp.request('GET', url,
                cookies={'test_cookie': 'value'}, loop=self.loop)
            self.assertEqual(200, response.status)
            data = yield from response.read_and_close()
            dct = json.loads(data.decode('utf-8'))
            self.assertEqual({'success': True,
                              'cookie': 'value',
                              }, dct)
        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())
