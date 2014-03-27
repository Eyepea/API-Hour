import unittest
from unittest import mock

import asyncio
import aiohttp
import email
from aiorest import RESTServer, Request, Response, PostJson
import json

from test.support import find_unused_port


def func(id, req: Request, resp: Response, post: PostJson):
    return {'success': True}


class RouterTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.server = RESTServer(debug=True, keep_alive=75,
                                 hostname='localhost', loop=self.loop)
        self.server.add_url('POST', '/post/{id}', func)
        self.server.add_url('GET', '/post/{id}', func)

    def tearDown(self):
        self.loop.close()

    def test_simple_POST(self):
        port = find_unused_port()

        svr = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/post/123'.format(port)

        def query():
            response = yield from aiohttp.request('POST', url, loop=self.loop)
            data = yield from response.read()
            self.assertEqual(b'{"success": true}', data)

        self.loop.run_until_complete(query())

        svr.close()
        self.loop.run_until_complete(svr.wait_closed())

    def test_simple_GET(self):
        port = find_unused_port()

        svr = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            'localhost', port))
        url = 'http://localhost:{}/post/123'.format(port)

        def query():
            response = yield from aiohttp.request('GET', url, loop=self.loop)
            data = yield from response.read()
            self.assertEqual(b'{"success": true}', data)

        self.loop.run_until_complete(query())

        svr.close()
        self.loop.run_until_complete(svr.wait_closed())
