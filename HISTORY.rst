CHANGES
=======

0.6.0 (2015-01-13)
------------------

* API-Hour config file is now optional, use -ac to auto-configure your app
* Add Python 3.3 compatibility to use easily Python 3 directly from distributions package
* Add Debian/Ubuntu package
* ujson is now optional for aiohttp.web
* More documentation with tutorials: all-in-one and Starter Kit
* If api_hour CLI has no logging file, enable logging on console by default

0.5.0 (2015-01-07)
------------------

* Project reboot
* Change API-Hour main goal: API-Hour can now multiprocess all AsyncIO lib server, not only HTTP
* API-Hour is now based on Gunicorn
* Remove aiorest fork, recommend to use aiohttp.web for HTTP daemons in cookiecutter

0.3.3 (2014-12-19)
------------------

* Static files can be served automatically
* body and json_body and transport accessible in Request
* loop accessible in Application
* Asset Serializer accepts encoding
* cookiecutter available at https://github.com/Eyepea/cookiecutter-API-Hour
* Use of ujson
* Bugfixes

0.3.2 (2014-10-31)
------------------

* Refactoring and clean-up
* Publish benchmark server for API-Hour
* English version of PyCON-FR presentation about API-Hour
* Fix response.write_eof() to follow aiohttp changes (Thanks aiorest for the patch)

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
