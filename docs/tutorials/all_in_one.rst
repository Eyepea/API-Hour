All-in-one Python script
========================

If you don't already install **API-Hour**, you can follow :ref:`installation` instructions.

Now, we're creating an API-Hour daemon that handles HTTP requests.

Create all_in_one.py file
-------------------------

.. literalinclude:: ../../examples/all_in_one.py
    :language: python

How to launch
-------------

In your current folder where you write your script, launch::

    api_hour all_in_one:Container

You'll see::

    [2015-01-12 23:17:02 +0100] [1763] [INFO] Starting gunicorn 19.1.1
    [2015-01-12 23:17:02 +0100] [1763] [INFO] Listening at: http://127.0.0.1:8000 (1763)
    [2015-01-12 23:17:02 +0100] [1763] [INFO] Using worker: api_hour.Worker
    [2015-01-12 23:17:02 +0100] [1766] [INFO] Booting worker with pid: 1766
    INFO:api_hour.container:Starting application...

Go to **http://127.0.0.1:8000/** to see the result of your index handler.

Benchmark the difference with several workers
---------------------------------------------

To use several workers::

    api_hour -w 16 all_in_one:Container

Compare the difference between one worker and several workers with **wrk**::

    wrk -t12 -c400 -d30s http://127.0.0.1:8000/

