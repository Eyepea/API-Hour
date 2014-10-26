api_hour
=======

Write performant WebServices with ease.

Install
-------

pip install api_hour

Mailing-list
------------

https://groups.google.com/d/forum/api-hour

Example usage
-------------

Simple REST server can be run like this::

   import asyncio
   import aiohttp
   import api_hour


   # define a simple request handler
   # which accept no arguments
   # and responds with json
   def hello(request):
       return {'hello': 'world'}


   loop = asyncio.get_event_loop()
   server = api_hour.Application(hostname='127.0.0.1',
                                 loop=loop)

   # configure routes
   server.add_url('GET', '/hello', hello)
   # create server
   srv = loop.run_until_complete(loop.create_server(
       server.make_handler, '127.0.0.1', 8080))


   @asyncio.coroutine
   def query():
       resp = yield from aiohttp.request(
           'GET', 'http://127.0.0.1:8080/hello', loop=loop)
       data = yield from resp.read_and_close(decode=True)
       print(data)


   loop.run_until_complete(query())
   srv.close()
   loop.run_until_complete(srv.wait_closed())
   loop.close()

this will print ``{'hello': 'world'}`` json

See `examples <https://github.com/Eyepea/API-Hour/tree/master/examples>`_ for more.


Requirements
------------

- Python 3.3

- asyncio http://code.google.com/p/tulip/ or Python 3.4+

- aiohttp http://github.com/KeepSafe/aiohttp

- optional module ``api_hour.redis_session`` requires aioredis
  https://github.com/aio-libs/aioredis

License
-------

api_hour is offered under the MIT license.
