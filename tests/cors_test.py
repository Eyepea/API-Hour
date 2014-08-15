import unittest
import asyncio
import aiohttp
import contextlib

from aiorest import RESTServer


class REST:

    def __init__(self, test):
        self.test = test

    def index(self, request):
        return {'status': 'ok'}

    def check_origin(self, request):
        return {'status': 'ok'}


class CorsTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.server = RESTServer(debug=True, hostname='localhost',
                                 enable_cors=True,
                                 loop=self.loop)
        add_url = self.server.add_url

        rest = REST(self)
        add_url('GET', '/', rest.index)
        add_url('GET', '/check_origin', rest.check_origin,
                cors_options={'allow-origin': 'http://example.com/'})

    def tearDown(self):
        self.loop.close()

    @contextlib.contextmanager
    def run_server(self):
        self.assertTrue(self.server.cors_enabled)

        srv = self.loop.run_until_complete(self.loop.create_server(
            self.server.make_handler,
            '127.0.0.1', 0))
        self.assertEqual(len(srv.sockets), 1)
        sock = next(iter(srv.sockets))
        host, port = sock.getsockname()
        self.assertEqual('127.0.0.1', host)
        self.assertGreater(port, 0)
        url = 'http://{}:{}'.format(host, port)
        yield url

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_simple_GET(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                headers = {
                    'ORIGIN': 'localhost',
                    }
                resp = yield from aiohttp.request('GET', url,
                                                  headers=headers,
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 200)
                self.assertIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)
                self.assertEqual(resp.headers['ACCESS-CONTROL-ALLOW-ORIGIN'],
                                 '*')

            self.loop.run_until_complete(query())

    def test_preflight(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                headers = {
                    'ACCESS-CONTROL-REQUEST-METHOD': 'GET',
                    'ORIGIN': 'localhost',
                    }
                resp = yield from aiohttp.request('OPTIONS', url,
                                                  headers=headers,
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 200)
                self.assertIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)
                self.assertEqual(resp.headers['ACCESS-CONTROL-ALLOW-ORIGIN'],
                                 '*')

            self.loop.run_until_complete(query())

    def test_preflight_404(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('OPTIONS', url,
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 404)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)

            self.loop.run_until_complete(query())

    def test_check_origin(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('GET', url + '/check_origin',
                                                  headers={},
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 200)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-METHOD', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-HEADERS', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-CREDENTIALS',
                                 resp.headers)

                headers = {
                    'ORIGIN': 'localhost',
                    }
                resp = yield from aiohttp.request('GET', url + '/check_origin',
                                                  headers=headers,
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 200)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-METHOD', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-HEADERS', resp.headers)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-CREDENTIALS',
                                 resp.headers)

                headers = {
                    'ORIGIN': 'http://example.com/',
                    }
                resp = yield from aiohttp.request('GET', url + '/check_origin',
                                                  headers=headers,
                                                  loop=self.loop)
                yield from resp.read()
                self.assertEqual(resp.status, 200)
                self.assertIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp.headers)

            self.loop.run_until_complete(query())
