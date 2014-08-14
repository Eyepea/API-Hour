import asyncio
import aiohttp
import aiorest
import json
from aiorest.session import CookieSessionFactory


class Handler:

    def __init__(self, limit=5):
        self.limit = limit

    @asyncio.coroutine
    def counter(self, req):
        session = yield from req.session
        if session.new:
            session['count'] = int(req.matchdict.get('start', 0))
        count = session['count'] + 1
        session['count'] = count
        if count >= self.limit:
            session.invalidate()
        return {'count': count}


def main():
    loop = asyncio.get_event_loop()

    handler = Handler()

    session_factory = CookieSessionFactory(secret_key=b'secret',
                                           cookie_name='test_cookie',
                                           dumps=json.dumps,
                                           loads=json.loads,
                                           loop=loop)

    server = aiorest.RESTServer(hostname='127.0.0.1', keep_alive=75,
                                session_factory=session_factory,
                                loop=loop)

    server.add_url('GET', '/count', handler.counter)

    srv = loop.run_until_complete(loop.create_server(
        server.make_handler, '127.0.0.1', 8080))

    @asyncio.coroutine
    def query():
        connector = aiohttp.TCPConnector(share_cookies=True, loop=loop)

        for _ in range(6):
            resp = yield from aiohttp.request(
                'GET', 'http://127.0.0.1:8080/count',
                connector=connector, loop=loop)
            data = yield from resp.json()
            print('Count is', data)

    loop.run_until_complete(query())

    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
