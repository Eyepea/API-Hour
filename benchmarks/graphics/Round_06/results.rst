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

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:18004/agents
    Running 30s test @ http://192.168.2.100:18004/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 35.063ms, rate sampling interval: 54ms
    Thread calibration: mean lat.: 47.197ms, rate sampling interval: 282ms
    Thread calibration: mean lat.: 43.657ms, rate sampling interval: 187ms
    Thread calibration: mean lat.: 36.359ms, rate sampling interval: 62ms
    Thread calibration: mean lat.: 45.731ms, rate sampling interval: 271ms
    Thread calibration: mean lat.: 32.571ms, rate sampling interval: 45ms
    Thread calibration: mean lat.: 44.982ms, rate sampling interval: 181ms
    Thread calibration: mean lat.: 44.792ms, rate sampling interval: 171ms
    Thread calibration: mean lat.: 33.758ms, rate sampling interval: 45ms
    Thread calibration: mean lat.: 45.126ms, rate sampling interval: 183ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    21.42ms    4.36ms  34.59ms   70.50%
        Req/Sec     0.96      3.81    22.00     96.30%
    300 requests in 30.01s, 2.09MB read
    Requests/sec:     10.00
    Transfer/sec:     71.16KB

uWSGI
'''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:28004/agents
    Running 30s test @ http://192.168.2.100:28004/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 36.906ms, rate sampling interval: 57ms
    Thread calibration: mean lat.: 35.255ms, rate sampling interval: 53ms
    Thread calibration: mean lat.: 41.797ms, rate sampling interval: 58ms
    Thread calibration: mean lat.: 38.114ms, rate sampling interval: 58ms
    Thread calibration: mean lat.: 61.522ms, rate sampling interval: 322ms
    Thread calibration: mean lat.: 39.784ms, rate sampling interval: 54ms
    Thread calibration: mean lat.: 30.692ms, rate sampling interval: 56ms
    Thread calibration: mean lat.: 42.445ms, rate sampling interval: 52ms
    Thread calibration: mean lat.: 48.009ms, rate sampling interval: 221ms
    Thread calibration: mean lat.: 63.519ms, rate sampling interval: 314ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    20.83ms    3.80ms  29.06ms   68.50%
        Req/Sec     0.98      3.91    19.00     94.88%
    300 requests in 30.01s, 2.09MB read
    Requests/sec:     10.00
    Transfer/sec:     71.16KB

Flask
-----

Meinheld
''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:18000/agents
    Running 30s test @ http://192.168.2.100:18000/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 20.746ms, rate sampling interval: 49ms
    Thread calibration: mean lat.: 21.563ms, rate sampling interval: 50ms
    Thread calibration: mean lat.: 21.311ms, rate sampling interval: 48ms
    Thread calibration: mean lat.: 21.359ms, rate sampling interval: 50ms
    Thread calibration: mean lat.: 19.786ms, rate sampling interval: 47ms
    Thread calibration: mean lat.: 19.856ms, rate sampling interval: 46ms
    Thread calibration: mean lat.: 19.154ms, rate sampling interval: 44ms
    Thread calibration: mean lat.: 19.366ms, rate sampling interval: 48ms
    Thread calibration: mean lat.: 18.850ms, rate sampling interval: 46ms
    Thread calibration: mean lat.: 18.956ms, rate sampling interval: 44ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    19.12ms    4.15ms  28.45ms   66.00%
        Req/Sec     0.99      4.45    23.00     95.27%
    300 requests in 30.01s, 2.08MB read
    Requests/sec:     10.00
    Transfer/sec:     71.00KB

uWSGI
'''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:28000/agents
    Running 30s test @ http://192.168.2.100:28000/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 18.773ms, rate sampling interval: 46ms
    Thread calibration: mean lat.: 18.828ms, rate sampling interval: 50ms
    Thread calibration: mean lat.: 17.250ms, rate sampling interval: 42ms
    Thread calibration: mean lat.: 17.959ms, rate sampling interval: 40ms
    Thread calibration: mean lat.: 17.770ms, rate sampling interval: 42ms
    Thread calibration: mean lat.: 18.126ms, rate sampling interval: 40ms
    Thread calibration: mean lat.: 18.062ms, rate sampling interval: 41ms
    Thread calibration: mean lat.: 17.825ms, rate sampling interval: 40ms
    Thread calibration: mean lat.: 17.279ms, rate sampling interval: 40ms
    Thread calibration: mean lat.: 16.860ms, rate sampling interval: 38ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    18.96ms    3.34ms  30.83ms   66.50%
        Req/Sec     1.00      4.80    27.00     95.82%
    300 requests in 30.01s, 2.08MB read
    Requests/sec:     10.00
    Transfer/sec:     71.00KB

API-Hour
--------

With Nginx
''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:18008/agents
    Running 30s test @ http://192.168.2.100:18008/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 9.313ms, rate sampling interval: 28ms
    Thread calibration: mean lat.: 8.348ms, rate sampling interval: 25ms
    Thread calibration: mean lat.: 9.005ms, rate sampling interval: 26ms
    Thread calibration: mean lat.: 8.768ms, rate sampling interval: 24ms
    Thread calibration: mean lat.: 8.694ms, rate sampling interval: 27ms
    Thread calibration: mean lat.: 9.118ms, rate sampling interval: 24ms
    Thread calibration: mean lat.: 9.039ms, rate sampling interval: 27ms
    Thread calibration: mean lat.: 8.121ms, rate sampling interval: 23ms
    Thread calibration: mean lat.: 7.546ms, rate sampling interval: 22ms
    Thread calibration: mean lat.: 7.834ms, rate sampling interval: 23ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     7.83ms    3.29ms  16.77ms   58.95%
        Req/Sec     0.96      6.21    47.00     97.63%
    310 requests in 30.00s, 1.94MB read
    Requests/sec:     10.33
    Transfer/sec:     66.24KB

Without Nginx
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8008/agents
    Running 30s test @ http://192.168.2.100:8008/agents
    10 threads and 10 connections
    Thread calibration: mean lat.: 7.224ms, rate sampling interval: 19ms
    Thread calibration: mean lat.: 7.177ms, rate sampling interval: 19ms
    Thread calibration: mean lat.: 6.685ms, rate sampling interval: 19ms
    Thread calibration: mean lat.: 6.644ms, rate sampling interval: 17ms
    Thread calibration: mean lat.: 7.582ms, rate sampling interval: 21ms
    Thread calibration: mean lat.: 6.610ms, rate sampling interval: 16ms
    Thread calibration: mean lat.: 6.529ms, rate sampling interval: 18ms
    Thread calibration: mean lat.: 6.936ms, rate sampling interval: 19ms
    Thread calibration: mean lat.: 7.568ms, rate sampling interval: 25ms
    Thread calibration: mean lat.: 6.999ms, rate sampling interval: 20ms
    Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     8.55ms    2.95ms  16.06ms   71.00%
        Req/Sec     1.02      7.33    66.00     98.08%
    307 requests in 30.01s, 1.92MB read
    Requests/sec:     10.23
    Transfer/sec:     65.64KB

