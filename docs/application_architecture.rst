Recommended architecture for your API-Hour Application
======================================================

*Nota bene: This architecture proposed is only a suggestion, based on our experience.*

MVC is a great pattern for User Interfaces made with Javascript, plain HTML, or Qt.

MVC is always adapted for Web client part with Javascript.

But, with WebServices API shift, from our point of view, MVC doesn't fit very well on server part, because:

1. You already have MVC pattern on client part, MVC on server becomes Model layer in your Javascript application.
2. With REST/JSON, you don't really need to have views (eg: templates), it's "only" JSON serialization.

API-Hour proposal
-----------------

In API-Hour, you have:

0. **Application**: An object that represents your application with everything inside: routing...
#. **Endpoints**: Simple Python functions called when your Application received a HTTP requests. It's functions because:
    #. Global state is stored in Application
    #. Reduce complexity
    #. Easier to share Endpoints between Application if it's only functions
#. **Engines**: Data source providers for Stores. Example: PostgreSQL, Asterisk, CouchDB...
#. **Stores**: Where you transform data for Endpoints. Like Endpoints, a Store is only a Python file with functions.

Examples
--------

In `examples <https://github.com/Eyepea/API-Hour/tree/master/examples>`_, you have a cookiecutter template to generate quickly your application.

You have also a real example with PostgreSQL integration in `benchmarks <https://github.com/Eyepea/API-Hour/tree/master/benchmarks/api_hour/benchmarks>`_.