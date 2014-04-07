import unittest
import asyncio
import aiohttp
import json
import contextlib

from aiorest import RESTServer
from aiorest.session import CookieSessionFactory

from test.support import find_unused_port


class REST:

    def __init__(self, test):
        self.test = test

    @asyncio.coroutine
    def init_session(self, req):
        sess = yield from req.session
        self.test.assertIsNotNone(sess)

    @asyncio.coroutine
    def get_from_session(self, req):
        sess = yield from req.session
        self.test.assertIsNotNone(sess)
        self.test.assertEqual(dict(sess), {'foo': 'bar'})
        sess['key'] = 'val'


class CookieSessionTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        session_factory = CookieSessionFactory(cookie_name='test_cookie',
                                               dumps=json.dumps,
                                               loads=json.loads,
                                               loop=self.loop)
        self.server = RESTServer(debug=True, keep_alive=75,
                                 hostname='localhost',
                                 session_factory=session_factory,
                                 loop=self.loop)
        rest = REST(self)

        self.server.add_url('GET', '/init', rest.init_session,
                            use_request='req')
        self.server.add_url('GET', '/get', rest.get_from_session,
                            use_request='req')

    def tearDown(self):
        self.loop.close()

    @contextlib.contextmanager
    def run_server(self):
        host = 'localhost'
        port = find_unused_port()
        srv = self.loop.run_until_complete(self.loop.create_server(
            lambda: self.server,
            host, port))
        base_url = 'http://{}:{}'.format(host, port)

        yield (srv, base_url)

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_get_from_session(self):
        with self.run_server() as (srv, base_url):

            url = base_url + '/get'

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('GET', url,
                    cookies={'test_cookie': json.dumps({'foo': 'bar'})},
                    loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 200)

            self.loop.run_until_complete(query())
