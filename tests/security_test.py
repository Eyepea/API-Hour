import unittest
import asyncio
import aiohttp

from aiorest import RESTServer
from aiorest.security import AbstractAuthorizationPolicy, CookieIdentityPolicy


def server_port(srv):
    sock = next(iter(srv.sockets))
    return sock.getsockname()[1]


class DictionaryAuthorizationPolicy(AbstractAuthorizationPolicy):
    def __init__(self, data):
        self.data = data

    @asyncio.coroutine
    def permits(self, identity, permission, context=None):
        record = self.data.get(identity)
        if record is not None:
            # TODO: implement actual permission checker
            if permission in record:
                return True
        return False

    @asyncio.coroutine
    def authorized_userid(self, identity):
        return identity if identity in self.data else None


class REST:

    @asyncio.coroutine
    def handler(self, request):
        identity = yield from request.identity_policy.identify(request)
        if not identity:
            return {'error': 'Identity not found'}

        userid = yield from request.auth_policy.authorized_userid(identity)
        if not userid:
            return {'error': 'User not found'}

        asked_permission = request.matchdict['permission']
        resp = yield from request.auth_policy.permits(
            identity, asked_permission
        )
        return {'allowed': resp}


class ServerTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        auth_policy = DictionaryAuthorizationPolicy({'chris': ('read',)})
        self.server = RESTServer(debug=True, keep_alive=75,
                                 hostname='127.0.0.1', loop=self.loop,
                                 identity_policy=CookieIdentityPolicy(),
                                 auth_policy=auth_policy)
        self.port = None
        rest = REST()
        self.server.add_url('GET', '/auth/{permission}', rest.handler)

    def tearDown(self):
        self.loop.close()

    def test_identity_missing(self):
        srv = self.loop.run_until_complete(self.loop.create_server(
                                           self.server.make_handler,
                                           '127.0.0.1', 0))
        self.port = port = server_port(srv)
        url = 'http://127.0.0.1:{}/auth'.format(port)

        def query():
            resp = yield from aiohttp.request(
                'GET', url+'/read',
                cookies={},
                loop=self.loop
            )
            json_data = yield from resp.json()
            self.assertEqual(json_data['error'], 'Identity not found')

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_user_missing(self):
        srv = self.loop.run_until_complete(self.loop.create_server(
                                           self.server.make_handler,
                                           '127.0.0.1', 0))
        self.port = port = server_port(srv)
        url = 'http://127.0.0.1:{}/auth'.format(port)

        def query():
            resp = yield from aiohttp.request(
                'GET', url+'/read',
                cookies={'userid': 'john'},  # not chris
                loop=self.loop
            )
            json_data = yield from resp.json()
            self.assertEqual(json_data['error'], 'User not found')

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_permission_missing(self):
        srv = self.loop.run_until_complete(self.loop.create_server(
                                           self.server.make_handler,
                                           '127.0.0.1', 0))
        self.port = port = server_port(srv)
        url = 'http://127.0.0.1:{}/auth'.format(port)

        def query():
            resp = yield from aiohttp.request(
                'GET', url+'/write',  # not read
                cookies={'userid': 'chris'},
                loop=self.loop
            )
            json_data = yield from resp.json()
            self.assertEqual(json_data['allowed'], False)

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())

    def test_permission_present(self):
        srv = self.loop.run_until_complete(self.loop.create_server(
                                           self.server.make_handler,
                                           '127.0.0.1', 0))
        self.port = port = server_port(srv)
        url = 'http://127.0.0.1:{}/auth'.format(port)

        def query():
            resp = yield from aiohttp.request(
                'GET', url+'/read',
                cookies={'userid': 'chris'},
                loop=self.loop
            )
            json_data = yield from resp.json()
            self.assertEqual(json_data['allowed'], True)

        self.loop.run_until_complete(query())

        srv.close()
        self.loop.run_until_complete(srv.wait_closed())
