import os
import asyncio
import aiohttp
import api_hour


class App(api_hour.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url('GET', '/hello-world', self.handler)
        self.add_url('GET', '/hello/{name}', self.say_hello)

    def handler(self, request):
        return {'hello': 'world'}

    def say_hello(self, request):
        return 'Hello, {}!'.format(request.matchdict['name'])


def main():
    loop = asyncio.get_event_loop()

    server = App(hostname='127.0.0.1', loop=loop)

    srv = loop.run_until_complete(loop.create_server(
        server.make_handler, '127.0.0.1', 8080))

    @asyncio.coroutine
    def query():
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/hello-world',
            loop=loop)
        json_data = yield from resp.json()
        print(json_data)

        name = os.environ.get('USER', 'John')
        resp = yield from aiohttp.request(
            'GET', 'http://127.0.0.1:8080/hello/{}'.format(name))

        json_data = yield from resp.json()
        print(json_data)

    loop.run_until_complete(query())
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
