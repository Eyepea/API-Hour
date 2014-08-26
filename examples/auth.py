import asyncio
import aiohttp
import aiorest

from aiorest.security import AbstractAuthorizationPolicy, CookieIdentityPolicy


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
    def authorized_user_id(self, identity):
        return identity if identity in self.data else None


@asyncio.coroutine
def handler(request):
    identity = yield from request.identity_policy.identify(request)
    if not identity:
        return {'error': 'Identity not found'}

    user_id = yield from request.auth_policy.authorized_user_id(identity)
    if not user_id:
        return {'error': 'User not found'}

    asked_permission = request.matchdict['permission']
    resp = yield from request.auth_policy.permits(
        identity, asked_permission,
    )
    return {'allowed': resp}


def main():
    loop = asyncio.get_event_loop()

    identity_policy = CookieIdentityPolicy()
    auth_policy = DictionaryAuthorizationPolicy({'chris': ('read',)})

    server = aiorest.RESTServer(
        hostname='127.0.0.1', loop=loop,
        identity_policy=identity_policy,
        auth_policy=auth_policy
    )
    server.add_url('GET', '/auth/{permission}', handler)

    srv = loop.run_until_complete(loop.create_server(
        server.make_handler, '127.0.0.1', 8080))

    @asyncio.coroutine
    def query():
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/auth/read',
            cookies={},
            loop=loop)
        json_data = yield from resp.json()
        assert json_data == {'error': 'Identity not found'}

        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/auth/read',
            cookies={'user_id': 'john'},
            loop=loop)
        json_data = yield from resp.json()
        assert json_data == {'error': 'User not found'}

        # correct user, must have read permission
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/auth/read',
            cookies={'user_id': 'chris'},
            loop=loop)
        json_data = yield from resp.json()
        assert json_data == {'allowed': True}

        # correct user, don't have write permission
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/auth/write',
            cookies={'user_id': 'chris'},
            loop=loop)
        json_data = yield from resp.json()
        assert json_data == {'allowed': False}

        print('Success')

    loop.run_until_complete(query())
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
