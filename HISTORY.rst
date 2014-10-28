CHANGES
=======

0.3.1 (2014-10-28)
------------------

* Rename multi_process to arbiter
* Improve Python packaging

0.3.0 (2014-10-26)
------------------

* First version of API-Hour, performance oriented version of aiorest
* cookiecutter template
* Serialization support
* replace json by ujson
* basic multiprocessing

0.2.4 (2014-09-12)
------------------

* Make loop keywork-only parameter in create_session_factory() function

0.2.3 (2014-08-28)
------------------

* Redis session switched from asyncio_redis to aioredis

0.2.2 (2014-08-15)
------------------

* Added Pyramid-like matchdict to request
  (see https://github.com/aio-libs/aiorest/pull/18)

* Return "400 Bad Request" for incorrect JSON body in POST/PUT methods

* README fixed

* Custom response status code
  (see https://github.com/aio-libs/aiorest/pull/23)


0.1.1 (2014-07-09)
------------------

* Switched to aiohttp v0.9.0


0.1.0 (2014-07-07)
------------------

* Basic REST API
