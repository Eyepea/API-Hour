API Hour
========

API-Hour is a lightweight daemon framework, that lets you write powerful applications.

It was created to answer the need for a simple, robust, and super-fast server-side environment to build very efficient Daemons with ease.

By default, API-Hour Starter Kit (Cookiecutter) creates for you a HTTP daemon to develop WebServices.

With API-Hour, you can quickly convert any AsyncIO server library to multi-processing daemon, ready for production.

.. image:: https://raw.githubusercontent.com/Eyepea/API-Hour/master/docs/API-Hour_small.png

Quick'n'dirty HTTP benchmarks on a kitchen table
------------------------------------------------

.. image:: https://raw.githubusercontent.com/Eyepea/API-Hour/master/propaganda/en/stats.png

Scale: Number of queries during 30 seconds with 400 simultaneous connexions.

Benchmark made on a Dell Precision M6800 between API-Hour and Gunicorn with 16 workers.

For details, read information in `benchmarks <https://github.com/Eyepea/API-Hour/tree/master/benchmarks>`_.

Where is the magic to have theses performances ?
''''''''''''''''''''''''''''''''''''''''''''''''

Architecture matters a lot more that tools.

We use asynchronous and multiprocess patterns, combined together, to handle as much as possible HTTP requests.

Ideally, the limitation should be your network card, not your CPU nor memory.

Moreover, we've tried to reduce as much as possible layers between your code and async sockets.

For each layer, we use the best in term of performance and simplicity:

#. `AsyncIO <https://docs.python.org/3/library/asyncio.html>`_: an easy asynchronous framework, directly integrated in Python 3.4+
#. `aiohttp.web <https://aiohttp.readthedocs.org/en/latest/web.html>`_: HTTP protocol implementation for AsyncIO + Web framework
#. `ujson <https://github.com/esnme/ultrajson#ultrajson>`_: fastest JSON serialization

Examples
--------

#. `API-Hour Starter Kit (Cookiecutter) <https://github.com/Eyepea/cookiecutter-API-Hour>`_
#. `API-Hour implementation of TechEmpower Web Framework Benchmarks <https://github.com/TechEmpower/FrameworkBenchmarks/tree/master/frameworks/Python/asyncio>`_
#. `HTTP+SSH Daemon <https://github.com/Eyepea/API-Hour/tree/master/examples/http_and_ssh>`_
#. `Quick'n'dirty benchmarks on a kitchen table <https://github.com/Eyepea/API-Hour/tree/master/benchmarks/api_hour/benchmarks>`_

How-to start an API-Hour project ?
----------------------------------

You can follow `one of our tutorials <https://pythonhosted.org/api_hour/tutorials/index.html>`_

Support
-------

* `Documentation <https://pythonhosted.org/api_hour/>`_.
* `Mailing-list <https://groups.google.com/d/forum/api-hour>`_

Requirements
------------

- Python 3.5+

Install
-------

Follow `official documentation <https://pythonhosted.org/api_hour/installation.html>`_.

License
-------

``API-Hour`` is offered under the Apache 2 license.

Architecture
------------

``API-Hour`` is a glue between your code and Gunicorn to launch your code in several process.

Origin
------

API-Hour was a fork of aiorest, now only based on Gunicorn for multiprocessing.

Thanks
------

Thanks to Gunicorn, aiorest, aiohttp and AsyncIO community, they made 99,9999% of the job for API-Hour.

Special thanks to **Andrew Svetlov**, the creator of aiorest.

Goals of API-Hour
-----------------

#. **Fast**: API-Hour is designed from bottom-up to be extremely fast, and capable of handling a huge load. It uses Python 3 and its new powerful AsyncIO package.
#. **Scalable**: API-Hour is built to be elastic, and easily scalable.
#. **Lightweight**:
    #. **small codebase**: Doing less means being faster: the codebase for processing an request is kept as small as possible. Beyond this base foot-print, you can of course activate, preload and initialize more plugins or packages , but that choice is yours.
    #. **flexible setup**: Some people have no problems with using many dependencies, while others want to have none (other than Python). Some people are ok to loose a bit on performance, for the ease (and speed) of coding, while others wouldn't sacrifice a millisecond  for ready-made functionality. These choices are yours, so there are no mandatory extra layer, plugin or middleware.
#. **Easy**: API-Hour is meant to be very easy to grasp: No steep learning curve, no mountain of docs to read: Download our turn-key "Hello-world" applications, and immediately start coding your own application from there.
#. **Packages-friendly and friendly-packages**: We try to let you use external packages without the need to re-write them, adapt them,  " wrap " them or embed them in the framework. On the other hand, API-Hour " plugins " are written as much as possible to be usable as stand-alone packages outside the framework, to benefit to more people.
#. **Asynchronous... or not**: If you don't need the extra complexity of building asynchronous code, you don't have to (you'll still enjoy tremendous performance). You can just handle your requests in a traditional synchronous way. On the other hand, if your project does IO or processing that could benefit from parallelizing tasks, the whole power of Async. IO, futures, coroutines and tasks is at your fingertips. All provided plugins (in particular, Database plugins) are Async-ready.

