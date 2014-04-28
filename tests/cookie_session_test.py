import unittest
import asyncio
import aiohttp
import json
import contextlib
import hashlib
import hmac

from aiorest import RESTServer
from aiorest.session import CookieSessionFactory

from unittest import mock


class REST:

    def __init__(self, test):
        self.test = test

    @asyncio.coroutine
    def init_session(self, req):
        sess = yield from req.session
        self.test.assertIsNotNone(sess)
        self.test.assertEqual(dict(sess), {})
        self.test.assertTrue(sess.new)
        sess['foo'] = 'bar'

    @asyncio.coroutine
    def get_from_session(self, req):
        sess = yield from req.session
        self.test.assertIsNotNone(sess)
        self.test.assertFalse(sess.new)
        self.test.assertIn('foo', sess)
        self.test.assertEqual(dict(sess), {'foo': 'bar'})

    @asyncio.coroutine
    def counter(self, req, start:int=0):
        sess = yield from req.session
        if sess.new:
            sess['result'] = start
        res = sess['result'] = sess['result'] + 1
        if res >= 5:
            sess.invalidate()
        return {'result': res}


def make_cookie(obj, timestamp):
    value = json.dumps(obj)
    timestamp = str(timestamp)
    parts = ('test_cookie', value, timestamp)
    h = hmac.new(b'secret', digestmod=hashlib.sha1)
    h.update(b'|'.join(map(lambda s: s.encode('utf-8'), parts)))
    sign = h.hexdigest()
    return '|'.join((value, timestamp, sign))


class CookieSessionTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        session_factory = CookieSessionFactory(secret_key=b'secret',
                                               cookie_name='test_cookie',
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
        self.server.add_url('GET', '/counter', rest.counter,
                            use_request='req')
        self.server.add_url('GET', '/counter/{start}', rest.counter,
                            use_request='req')

    def tearDown(self):
        self.loop.close()

    @contextlib.contextmanager
    def run_server(self):
        srv = self.loop.run_until_complete(self.loop.create_server(
            self.server.make_handler,
            'localhost', 0))
        sock = next(iter(srv.sockets))
        port = sock.getsockname()[1]
        base_url = 'http://localhost:{}'.format(port)

        yield (srv, base_url)

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    @mock.patch('aiorest.session.time')
    def test_init_session(self, time_mock):
        time_mock.time.return_value = 1
        with self.run_server() as (srv, base_url):
            url = base_url + '/init'

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('GET', url, loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 200)
                cookies = {k: v.value for k, v in resp.cookies.items()}
                value = make_cookie({'foo': 'bar'}, 1)
                self.assertEqual(cookies, {'test_cookie': value})

            self.loop.run_until_complete(query())

    @mock.patch('aiorest.session.time')
    def test_get_from_session(self, time_mock):
        time_mock.time.return_value = 1
        with self.run_server() as (srv, base_url):

            url = base_url + '/get'

            @asyncio.coroutine
            def query():
                resp = yield from aiohttp.request('GET', url,
                    cookies={'test_cookie': make_cookie({'foo': 'bar'}, 1)},
                    loop=self.loop)
                yield from resp.read_and_close()
                self.assertEqual(resp.status, 200)

            self.loop.run_until_complete(query())

    def test_full_cycle(self):
        with self.run_server() as (srv, base_url):
            url = base_url + '/counter'

            @asyncio.coroutine
            def queries():
                connector = aiohttp.SocketConnector(share_cookies=True,
                                                    loop=self.loop)
                # initiate session; set start value to 2
                resp = yield from aiohttp.request('GET', url + "/2",
                    connector=connector, loop=self.loop)
                data = yield from resp.read_and_close(decode=True)
                self.assertEqual(resp.status, 200)
                self.assertEqual(data, {'result': 3})

                # do increment
                resp = yield from aiohttp.request('GET', url,
                    connector=connector, loop=self.loop)
                data = yield from resp.read_and_close(decode=True)
                self.assertEqual(resp.status, 200)
                self.assertEqual(data, {'result': 4})

                # try to override start value
                resp = yield from aiohttp.request('GET', url + '/3',
                    connector=connector, loop=self.loop)
                data = yield from resp.read_and_close(decode=True)
                self.assertEqual(resp.status, 200)
                self.assertEqual(data, {'result': 5})

                # session deleted; try count
                resp = yield from aiohttp.request('GET', url,
                    connector=connector, loop=self.loop)
                data = yield from resp.read_and_close(decode=True)
                self.assertEqual(resp.status, 200)
                self.assertEqual(data, {'result': 1})

            self.loop.run_until_complete(queries())
