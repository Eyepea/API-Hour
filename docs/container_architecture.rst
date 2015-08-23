.. _container_architecture:

Recommended architecture for your API-Hour Container
====================================================

*Nota bene: This architecture proposed is only a suggestion, based on our experience.*

MVC is a great pattern for User Interfaces made with Javascript, plain HTML, or Qt.

MVC is always adapted for Web client part with Javascript.

But, with WebServices API shift, from our point of view, MVC doesn't fit very well on server part, because:

1. You already have MVC pattern on client part, MVC on server becomes Model layer in your Javascript application.
2. With REST/JSON, you don't really need to have views (eg: templates), it's "only" JSON serialization.

Moreover, if you build a Daemon without an UI, like a SSH server, MVC doesn't fit very well.

API-Hour proposal: Program with EASE
------------------------------------

EASE = Endpoints for APIs, Services and Engines

In API-Hour, you have:

0. **Container**: An object that represents your application with everything inside: routing...
#. **Endpoints**: Simple Python coroutines called when your Application received requests (HTTP, SSH...). It's coroutines because:
    #. Global state is stored in Container
    #. Reduce complexity
    #. Easier to share Endpoints between Containers if it's only coroutines
#. **Engines**: Data source providers for Services. Example: PostgreSQL, Asterisk, CouchDB...
#. **Services**: Where you transform data for Endpoints. Like Endpoints, a Service is only a Python file with coroutines. It represents your business logic and your internal Python API. You should see this part like microservices without internal HTTP communications that reduce the global efficiency.
