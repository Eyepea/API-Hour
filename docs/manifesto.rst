Manifesto
=========

The API paradigm shift
----------------------

Over the last few years, the web has deeply changed. Browsers are more sophisticated than ever, javascript engines are finally showing good performances, and large client-side (javascript) frameworks are now bringing easy cross-browser compatibility. They also ease the building of nice and complex GUIs, they compensate for most of the language  weaknesses and nowadays, they even provide structuring patterns like MVC on the client side.

Meanwhile, more and more services are provided " in the cloud ", and there are more and more software as a service (SaaS) and whit-labeling is everywhere.

We see three main consequences there:

#. Traditional web-sites had to provide more interactive and user-friendly pages, drifting away from the submit-refresh paradigm, towards Ajax-only pages.
#. Client-side programming is becoming more and more GUI programming.
#. The need for service-to-service (thus server-to-server ) interconnections is increasing quickly, meaning that the server-side needs have now shifted towards providing an API.

We believe that providing an API built " on top of " or " alongside " traditional web is no longer a wise option.

Nowadays, your web-application should rely solely on your API, the very same API that you will expose to third parties. If your API works 100% for you, it will work 100% for them. If you API covers 100% of the service needs for your, it will cover 100% of their needs as well. Any new feature requested or provided in the API immediately benefits to everyone.

Over the last few years, we therefore abandoned completely old-fashioned web-apps, in favor of this GUI-API model for all our projects, with pleasure and success while enjoying better efficiency, and faster deliveries.

Better emerging standards: JSON and RESTful

In the early days of homo-informaticus, protocols defining bunches of semi-organized bytes only their author could really comprehend. As transmission was slow and costly, they super-optimized, and super un-intelligible.

In the early-days of homo-internetus, bandwidth became widely available. Protocols then became very verbose, even grandma could read them. One of them, the diplodocus of protocolas was called Xtra-Massive and Large. Some protocols where created to describe themselves in the vague hope that machines would program themselves and steal the poor developer's jobs. Some of these creatures like the Xtra-Savage-Lobotomising-terror  were feared as they were known to eat developer's brains.

Hopefully natural selection took place and we now have protocols and encoding which are both slim, readable, and harmless like Json or UTF-8.

Making typical API HTTP requests (CRUD) with JSON on logical URLs is also done following a standard that naturally emerged. It is called RESTful.

No competition but complementarity
----------------------------------

We had a Twisted-hammer and we loved it. Everything was a nail. We had a lot of real-time protocols to make, so we hammered them like crazy with Twisted and it worked great.

We had a Django-hammer and we loved it. Everything was a nail. We had a lot of dynamic websites to beat down, and a lot of database-management interfaces to explode, so we hammered them with Django and it was great.

After all this work, we were thirsty, so we used flask to cool off, and it was great.

Then we wanted a dedicated tool for API construction.

We didn't want an accessory to plug onto any of our other tools, because that would have made it too heavy. (good hammers adapted to developer's hands are not very heavy)

We wanted something efficient as a hammer, fast as a cheetah, light as a feather, easy like a sunday morning, and delightful as a cocktail.

So we wrote API-Hour and it is great.

After a while, we shift from HTTP-centric point of view to any protocol.