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

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:18004/agents
    Running 5m test @ http://192.168.2.100:18004/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 81.758ms, rate sampling interval: 529ms
    Thread calibration: mean lat.: 81.794ms, rate sampling interval: 531ms
    Thread calibration: mean lat.: 88.885ms, rate sampling interval: 542ms
    Thread calibration: mean lat.: 108.880ms, rate sampling interval: 580ms
    Thread calibration: mean lat.: 97.797ms, rate sampling interval: 569ms
    Thread calibration: mean lat.: 107.733ms, rate sampling interval: 605ms
    Thread calibration: mean lat.: 230.035ms, rate sampling interval: 1559ms
    Thread calibration: mean lat.: 87.710ms, rate sampling interval: 548ms
    Thread calibration: mean lat.: 79.446ms, rate sampling interval: 523ms
    Thread calibration: mean lat.: 83.200ms, rate sampling interval: 547ms
    Thread calibration: mean lat.: 80.636ms, rate sampling interval: 531ms
    Thread calibration: mean lat.: 98.565ms, rate sampling interval: 646ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   121.08ms  204.06ms   2.66s    86.91%
        Req/Sec   332.74     22.85   423.00     71.00%
    1197819 requests in 5.00m, 1.46GB read
    Non-2xx or 3xx responses: 1031238
    Requests/sec:   3992.68
    Transfer/sec:      4.97MB

uWSGI
'''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:28004/agents
    Running 5m test @ http://192.168.2.100:28004/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 56.112ms, rate sampling interval: 396ms
    Thread calibration: mean lat.: 68.605ms, rate sampling interval: 428ms
    Thread calibration: mean lat.: 77.111ms, rate sampling interval: 483ms
    Thread calibration: mean lat.: 63.422ms, rate sampling interval: 522ms
    Thread calibration: mean lat.: 70.246ms, rate sampling interval: 430ms
    Thread calibration: mean lat.: 73.056ms, rate sampling interval: 455ms
    Thread calibration: mean lat.: 37.092ms, rate sampling interval: 287ms
    Thread calibration: mean lat.: 78.166ms, rate sampling interval: 502ms
    Thread calibration: mean lat.: 79.519ms, rate sampling interval: 490ms
    Thread calibration: mean lat.: 79.956ms, rate sampling interval: 517ms
    Thread calibration: mean lat.: 78.398ms, rate sampling interval: 500ms
    Thread calibration: mean lat.: 73.395ms, rate sampling interval: 461ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    72.71ms  131.98ms   2.29s    83.46%
        Req/Sec   332.90     23.29   432.00     75.41%
    1197779 requests in 5.00m, 1.47GB read
    Non-2xx or 3xx responses: 1029213
    Requests/sec:   3991.96
    Transfer/sec:      5.02MB

Flask
-----

Meinheld
''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:18000/agents
    Running 5m test @ http://192.168.2.100:18000/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 96.139ms, rate sampling interval: 573ms
    Thread calibration: mean lat.: 58.715ms, rate sampling interval: 477ms
    Thread calibration: mean lat.: 116.286ms, rate sampling interval: 697ms
    Thread calibration: mean lat.: 108.372ms, rate sampling interval: 672ms
    Thread calibration: mean lat.: 99.052ms, rate sampling interval: 596ms
    Thread calibration: mean lat.: 104.883ms, rate sampling interval: 627ms
    Thread calibration: mean lat.: 104.134ms, rate sampling interval: 630ms
    Thread calibration: mean lat.: 95.964ms, rate sampling interval: 572ms
    Thread calibration: mean lat.: 114.037ms, rate sampling interval: 686ms
    Thread calibration: mean lat.: 55.012ms, rate sampling interval: 472ms
    Thread calibration: mean lat.: 120.368ms, rate sampling interval: 715ms
    Thread calibration: mean lat.: 103.603ms, rate sampling interval: 576ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   111.29ms  183.07ms   2.37s    86.58%
        Req/Sec   332.78     22.05   425.00     72.00%
    1197627 requests in 5.00m, 1.50GB read
    Non-2xx or 3xx responses: 1024192
    Requests/sec:   3991.43
    Transfer/sec:      5.12MB

uWSGI
'''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:28000/agents
    Running 5m test @ http://192.168.2.100:28000/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 54.106ms, rate sampling interval: 376ms
    Thread calibration: mean lat.: 52.887ms, rate sampling interval: 370ms
    Thread calibration: mean lat.: 55.571ms, rate sampling interval: 378ms
    Thread calibration: mean lat.: 55.419ms, rate sampling interval: 379ms
    Thread calibration: mean lat.: 56.577ms, rate sampling interval: 377ms
    Thread calibration: mean lat.: 53.174ms, rate sampling interval: 376ms
    Thread calibration: mean lat.: 65.971ms, rate sampling interval: 401ms
    Thread calibration: mean lat.: 53.039ms, rate sampling interval: 374ms
    Thread calibration: mean lat.: 49.950ms, rate sampling interval: 371ms
    Thread calibration: mean lat.: 51.171ms, rate sampling interval: 372ms
    Thread calibration: mean lat.: 58.185ms, rate sampling interval: 385ms
    Thread calibration: mean lat.: 58.564ms, rate sampling interval: 382ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    65.98ms  116.59ms   1.68s    80.90%
        Req/Sec   332.95     20.88   417.00     69.93%
    1198372 requests in 5.00m, 1.52GB read
    Non-2xx or 3xx responses: 1021953
    Requests/sec:   3994.09
    Transfer/sec:      5.18MB

API-Hour
--------

With Nginx
''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:18008/agents
    Running 5m test @ http://192.168.2.100:18008/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 40.850ms, rate sampling interval: 125ms
    Thread calibration: mean lat.: 41.892ms, rate sampling interval: 126ms
    Thread calibration: mean lat.: 38.033ms, rate sampling interval: 124ms
    Thread calibration: mean lat.: 40.574ms, rate sampling interval: 125ms
    Thread calibration: mean lat.: 41.720ms, rate sampling interval: 126ms
    Thread calibration: mean lat.: 44.780ms, rate sampling interval: 128ms
    Thread calibration: mean lat.: 45.246ms, rate sampling interval: 127ms
    Thread calibration: mean lat.: 41.915ms, rate sampling interval: 124ms
    Thread calibration: mean lat.: 41.521ms, rate sampling interval: 126ms
    Thread calibration: mean lat.: 41.169ms, rate sampling interval: 125ms
    Thread calibration: mean lat.: 39.114ms, rate sampling interval: 126ms
    Thread calibration: mean lat.: 38.836ms, rate sampling interval: 126ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    43.07ms   27.47ms 202.11ms   61.35%
        Req/Sec   334.00     26.82   443.00     69.01%
    1198477 requests in 5.00m, 5.52GB read
    Non-2xx or 3xx responses: 312600
    Requests/sec:   3994.96
    Transfer/sec:     18.83MB

Without Nginx
'''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8008/agents
    Running 5m test @ http://192.168.2.100:8008/agents
    12 threads and 400 connections
    Thread calibration: mean lat.: 179.566ms, rate sampling interval: 1011ms
    Thread calibration: mean lat.: 165.892ms, rate sampling interval: 966ms
    Thread calibration: mean lat.: 167.430ms, rate sampling interval: 970ms
    Thread calibration: mean lat.: 156.925ms, rate sampling interval: 920ms
    Thread calibration: mean lat.: 175.077ms, rate sampling interval: 1021ms
    Thread calibration: mean lat.: 177.112ms, rate sampling interval: 966ms
    Thread calibration: mean lat.: 145.486ms, rate sampling interval: 802ms
    Thread calibration: mean lat.: 179.665ms, rate sampling interval: 994ms
    Thread calibration: mean lat.: 165.773ms, rate sampling interval: 895ms
    Thread calibration: mean lat.: 173.477ms, rate sampling interval: 1052ms
    Thread calibration: mean lat.: 131.386ms, rate sampling interval: 799ms
    Thread calibration: mean lat.: 197.082ms, rate sampling interval: 1084ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     9.74s    19.14s    1.72m    85.80%
        Req/Sec   303.21     13.19   352.00     73.40%
    1093835 requests in 5.00m, 6.69GB read
    Requests/sec:   3646.15
    Transfer/sec:     22.85MB

