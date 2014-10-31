API Hour
========

API-Hour is a lightweight webservices framework,  that lets you write powerful APIs for web applications.
It uses a simplified form of the MVC pattern. (with serializers instead of views).
It was created to answer the need for a simple, robust, and super-fast server-side environment to build very efficient WebServices with ease.

.. image:: https://raw.githubusercontent.com/Eyepea/API-Hour/master/docs/API-Hour_small.png

Benchmarks on the kitchen table
-------------------------------

.. image:: https://raw.githubusercontent.com/Eyepea/API-Hour/master/propaganda/en/stats.png

For details, read information in `benchmarks <https://github.com/Eyepea/API-Hour/tree/master/benchmarks>`_.

Where is the magic to have theses performances ?
''''''''''''''''''''''''''''''''''''''''''''''''

Architecture matters a lot more that tools.

We use asynchronous and multiprocess patterns, combined together, to handle as much as possible HTTP requests.

Ideally, the limitation should be your network card, not your CPU nor memory.

Moreover, we've tried to reduce as much as possible layers between your code and async sockets.

For each layer, we use the best in term of performances and simplicity:

1. AsyncIO: an easy asynchronous framework, directly integrated in Python 3.4+
2. aiohttp: HTTP protocol implementation for AsyncIO
3. ujson: fastest JSON serialization

Install
-------

pip install api_hour

Mailing-list
------------

https://groups.google.com/d/forum/api-hour

Example usages
--------------

See `examples <https://github.com/Eyepea/API-Hour/tree/master/examples>`_ for more.

In **examples/**, you have also a cookiecutter template to generate quickly your application.

Requirements
------------

- Python 3.4.2+

- `aiohttp <http://github.com/KeepSafe/aiohttp>`_

- optional module ``api_hour.redis_session`` requires `aioredis <https://github.com/aio-libs/aioredis>`_

License
-------

API-Hour is offered under the MIT license.

Origin
------

API-Hour is a performance oriented version of aiorest.

Why you don't contribute in aiorest instead of make your fork ?
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

We tried, but we wanted to add in aiorest some features that aiorest don't wish to integrate.

Nevertheless, aiorest and API-Hour have the same roots with aiohttp, we contribute together inside aiohttp.

Thanks
------

Thanks to aiorest, aiohttp and AsyncIO community, they made 99,9999% of the job for API-Hour.

Special thanks to **Andrew Svetlov**, the creator of aiorest.

Goals of API-Hour
-----------------

1. **Fast**: API-Hour is designed from bottom-up to be extremely fast, and capable of handling a huge load. It uses Python 3 and its new powerful AsyncIO package.
2. **Scalable**: API-Hour is built to be elastic, and easily scalable.
3. **Lightweight**:
    1. **small codebase**: Doing less means being faster: the codebase for processing an HTTP request is kept as small as possible. Beyond this base foot-print, you can of course activate, preload and initialize more plugins or packages , but that choice is yours.
    2. **flexible setup**: Some people have no problems with using many dependencies, while others want to have none (other thant Python). Some people are ok to loose a bit on performance, for the ease (and speed) of coding, while others wouldn't sacrifice a millisecond  for ready-made functionality. These choices are yours, so there are no mandatory extra layer, plugin or middleware.
4. **Easy**: API-Hour is meant to be very easy to grasp: No steep learning curve, no mountain of docs to read: Download our turn-key «Hello-world» applications, and immediately start coding your own application from there.
5. **Packages-friendly and friendly-packages**: We try to let you use external packages without the need to re-write them, adapt them,  « wrap » them or embed them in the framework. On the other hand, API-Hour « plugins » are written as much as possible to be usable as stand-alone packages outside the framework, to benefit to more people.
6. **Asynchronous... or not**: If you don't need the extra complexity of building asynchronous code, you don't have to (you'll still enjoy tremendous performance). You can just handle your requests in a traditional synchronous way. On the other hand, if your project does IO or processing that could benefit from parallelizing tasks, the whole power of Async. IO, futures, coroutines and tasks is at your fingertips. All provided plugins (in particular, Database plugins) are Async-ready.

What it is not
--------------

API-Hour is not a framework meant to generate HTML pages.
If you are looking for a framework that will help you build things like Forums, Blogs, CMSes , Database applications...  keeping the traditional submit => refresh paradigm, then you might want to take a look at frameworks like Django or Flask.
Both are widely used, they have plenty of plugins and they both use a powerful templating system to generate your pages.

Why another web framework ?
---------------------------

There are already a number of web frameworks available, and several of them are well known known and proven solutions in Python. We used them for small and bigger real-life projects. So where is the need for a new one ?

The API paradigm shift
''''''''''''''''''''''

Over the last few years, the web has deeply changed. Browsers are more sophisticated than ever, javascript engines are finally showing good performances, and large client-side (javascript) frameworks are now bringing easy cross-browser compatibility. They also ease the building of nice and complex GUIs, they compensate for most of the language  weaknesses and nowadays, they even provide structuring patterns like MVC on the client side.

Meanwhile, more and more services are provided « in the cloud », and there are more and more software as a service (SaaS) and whit-labeling is everywhere.

We see three main consequences there:

1. Traditional web-sites had to provide more interactive and user-friendly pages, drifting away from the submit-refresh paradigm, towards Ajax-only pages.
2. Client-side programming is becoming more and more GUI programming.
3. The need for service-to-service (thus server-to-server ) interconnections is increasing quickly, meaning that the server-side needs have now shifted towards providing an API.

We believe that providing an API built « on top of » or « alongside » traditional web is no longer a wise option.

Nowadays, your web-application should rely solely on your API, the very same API that you will expose to third parties. If your API works 100% for you, it will work 100% for them. If you API covers 100% of the service needs for your, it will cover 100% of their needs as well. Any new feature requested or provided in the API immediately benefits to everyone.

Over the last few years, we therefore abandoned completely old-fashioned web-apps, in favor of this GUI-API model for all our projects, with pleasure and success while enjoying better efficiency, and faster deliveries.

Better emerging standards: JSON and RESTful

In the early days of homo-informaticus, protocols defining bunches of semi-organized bytes only their author could really comprehend. As transmission was slow and costly, they super-optimized, and super un-intelligible.

In the early-days of homo-internetus, bandwidth became widely available. Protocols then became very verbose, even grandma could read them. One of them, the diplodocus of protocolas was called Xtra-Massive and Large. Some protocols where created to describe themselves in the vague hope that machines would program themselves and steal the poor developer's jobs. Some of these creatures like the Xtra-Savage-Lobotomising-terror  were feared as they were known to eat developer's brains.

Hopefully natural selection took place and we now have protocols and encoding which are both slim, readable, and harmless like Json or UTF-8.

Making typical API HTTP requests (CRUD) with Json on logical URLs is also done following a standard that naturally emerged. It is called RESTful.

No competition but complementarity
''''''''''''''''''''''''''''''''''

We had a Twisted-hammer and we loved it. Everything was a nail. We had a lot of real-time protocols to make, so we hammered them like crazy with Twisted and it worked great.

We had a Django-hammer and we loved it. Everything was a nail. We had a lot of dynamic websites to beat down, and a lot of database-management interfaces to explode, so we hammered them with Django and it was great.

After all this work, we were thirsty, so we used flask to cool off, and it was great.

Then we wanted a dedicated tool for API construction.

We didn't want an accessory to plug onto any of our other tools, because that would have made it too heavy. (good hammers adapted to developer's hands are not very heavy)

We wanted something efficient as a hammer, fast as a cheetah, light as a feather, easy like a sunday morning, and delightful as a cocktail.

So we wrote API-Hour and it is great.
