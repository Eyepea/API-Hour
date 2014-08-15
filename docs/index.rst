.. aiorest documentation master file, created by
   sphinx-quickstart on Fri Mar 14 19:59:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _GitHub: https://github.com/aio-libs/aiorest


aiorest
=======

aiorest is a minimalistic framework to build JSON REST server.

Features
--------

- URL routing
- URL parameters matching and type check through annotations
- Cookie-based sessions
- Redis-based sessions
- Cross-origin resource sharing (CORS) support

Installation
------------

The library can be installed by executing::

    pip3 install aiorest

Source code
-----------

The project is hosted on GitHub_

Please feel free to file an issue on `bug tracker
<https://github.com/aio-libs/aiorest/issues>`_ if you have found a bug
or have some suggestion for library improvement.

Dependencies
------------

- Python 3.3 and :term:`asyncio` or Python 3.4+
- :term:`aiohttp` 0.7.2+
- ``aiorest.redis_session`` requires :term:`asyncio-redis` 0.12.3+

License
-------

The project is licensed under the MIT license.

Getting started
---------------

Simple "hello world" REST server would look like this::

    import asyncio
    import aiorest

    def hello(request):
        return {'hello': 'world'}

    loop = asyncio.get_event_loop()
    srv = aiorest.RESTServer(hostname='127.0.0.1',
                                loop=loop)

    srv.add_url('GET', '/hello', hello)
    server = loop.run_until_complete(loop.create_server(
        srv.make_handler, '127.0.0.1', 8080))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        loop.run_until_complete(server.wait_closed())
        loop.close()

And simple aiohttp client request::

    import asyncio
    import aiohttp

    @asyncio.coroutine
    def go():
        resp = yield from aiohttp.request('GET', 'http://127.0.0.1:8080/hello')
        data = yield from resp.read_and_close(decode=True)
        print(data)

    asyncio.get_event_loop().run_until_complete(go())
    # this would print {'hello': 'world'}


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::

   examples
