Command line used to launch daemons
===================================

Django
------

Meinheld
''''''''

::

    $ gunicorn --workers 16 -b 0.0.0.0:8004 -k meinheld.gmeinheld.MeinheldWorker -b unix:/tmp/django.sock benchmarks.wsgi

uWSGI
'''''

::

    $ uwsgi --ini ../uwsgi.ini --processes 16 --wsgi benchmarks.wsgi

Flask
-----

Meinheld
''''''''

::

    $ gunicorn --workers 16 -b 0.0.0.0:8000 -k meinheld.gmeinheld.MeinheldWorker -b unix:/tmp/flask.sock application:app

uWSGI
'''''

::

    $ uwsgi --ini uwsgi.ini --processes 16 --wsgi application:app

API-Hour
--------

::

    $ api_hour -ac -b unix:/tmp/api_hour.sock -b 0.0.0.0:8008 benchmarks:Container

Results
=======

Django
------

Meinheld
''''''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:18004/agents
    Running 5m test @ http://192.168.2.100:18004/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    79.77ms   11.37ms 161.01ms   74.49%
        Req/Sec    49.83      2.72    60.00     67.62%
    180927 requests in 5.00m, 1.23GB read
    Requests/sec:    603.07
    Transfer/sec:      4.19MB

uWSGI
'''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:28004/agents
    Running 5m test @ http://192.168.2.100:28004/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    79.58ms   10.48ms 148.58ms   74.15%
        Req/Sec    49.92      2.70    63.00     68.73%
    181022 requests in 5.00m, 1.23GB read
    Requests/sec:    603.38
    Transfer/sec:      4.19MB

Flask
-----

Meinheld
''''''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:18000/agents
    Running 5m test @ http://192.168.2.100:18000/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    77.05ms    9.55ms 156.66ms   73.72%
        Req/Sec    51.62      5.42    78.00     70.69%
    187169 requests in 5.00m, 1.27GB read
    Requests/sec:    623.85
    Transfer/sec:      4.33MB

uWSGI
'''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:28000/agents
    Running 5m test @ http://192.168.2.100:28000/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    76.55ms    9.66ms 139.15ms   73.64%
        Req/Sec    52.04      5.55    73.00     70.25%
    188579 requests in 5.00m, 1.28GB read
    Requests/sec:    628.58
    Transfer/sec:      4.36MB

API-Hour
--------

With Nginx
''''''''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:18008/agents
    Running 5m test @ http://192.168.2.100:18008/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    16.10ms    8.00ms 111.28ms   71.90%
        Req/Sec   255.09     41.46   465.00     67.25%
    909953 requests in 5.00m, 5.56GB read
    Requests/sec:   3033.17
    Transfer/sec:     18.99MB

Without Nginx
'''''''''''''

::

    $ wrk -t12 -c50 -d5m http://192.168.2.100:8008/agents
    Running 5m test @ http://192.168.2.100:8008/agents
    12 threads and 50 connections
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    13.98ms    8.50ms 142.51ms   70.95%
        Req/Sec   310.23     89.33   742.00     67.90%
    1083287 requests in 5.00m, 6.63GB read
    Requests/sec:   3610.96
    Transfer/sec:     22.62MB

