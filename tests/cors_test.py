import unittest
import asyncio
import aiohttp
import contextlib

from aiorest import RESTServer


class REST:

    def __init__(self, test):
        self.test = test

    def index(self):
        return 'ok'


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

    def tearDown(self):
        self.loop.close()

    @contextlib.contextmanager
    def run_server(self):
        self.assertTrue(self.server.cors_enabled)

        srv = self.loop.run_until_complete(self.loop.create_server(
            self.server.make_handler,
            'localhost', 0))
        sock = next(iter(srv.sockets))
        port = sock.getsockname()[1]
        url = 'http://localhost:{}'.format(port)
        yield url

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_simple_GET(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('GET', url, loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 200)
                self.assertIn('ACCESS-CONTROL-ALLOW-METHODS', resp)
                self.assertEqual(resp['ACCESS-CONTROL-ALLOW-METHODS'], 'GET')
                self.assertIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp)
                self.assertEqual(resp['ACCESS-CONTROL-ALLOW-ORIGIN'], '*')

            self.loop.run_until_complete(query())

    def test_preflight(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                headers = {
                    'ACCESS-CONTROL-REQUEST-METHOD': 'GET',
                    }
                resp = yield from aiohttp.request('OPTIONS', url,
                                                  headers=headers,
                                                  loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 200)
                self.assertIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp)
                self.assertEqual(resp['ACCESS-CONTROL-ALLOW-ORIGIN'], '*')

            self.loop.run_until_complete(query())

    def test_preflight_404(self):
        with self.run_server() as url:

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('OPTIONS', url,
                                                  loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 404)
                self.assertNotIn('ACCESS-CONTROL-ALLOW-ORIGIN', resp)

            self.loop.run_until_complete(query())
