Command line used to launch WSGI server
=======================================

::

    gunicorn -w 16 -b 0.0.0.0:8004 benchmarks.wsgi

JSON Serialization only
=======================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8004/index
    Running 30s test @ http://127.0.0.1:8004/index
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     7.70s     6.43s   13.27s    58.89%
        Req/Sec   147.91    270.77     1.61k    86.86%
      70598 requests in 30.12s, 14.68MB read
      Socket errors: connect 396, read 0, write 0, timeout 4093
    Requests/sec:   2344.23
    Transfer/sec:    499.06KB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8004/index
    Running 5m test @ http://192.168.2.100:8004/index
      12 threads and 400 connections
      Thread calibration: mean lat.: 1237.280ms, rate sampling interval: 6041ms
      Thread calibration: mean lat.: 1438.455ms, rate sampling interval: 7208ms
      Thread calibration: mean lat.: 1554.853ms, rate sampling interval: 8396ms
      Thread calibration: mean lat.: 1470.193ms, rate sampling interval: 7417ms
      Thread calibration: mean lat.: 1344.203ms, rate sampling interval: 6680ms
      Thread calibration: mean lat.: 1784.472ms, rate sampling interval: 11780ms
      Thread calibration: mean lat.: 2033.932ms, rate sampling interval: 10223ms
      Thread calibration: mean lat.: 1792.615ms, rate sampling interval: 11354ms
      Thread calibration: mean lat.: 1485.402ms, rate sampling interval: 13549ms
      Thread calibration: mean lat.: 1800.163ms, rate sampling interval: 10182ms
      Thread calibration: mean lat.: 1290.032ms, rate sampling interval: 8339ms
      Thread calibration: mean lat.: 1332.951ms, rate sampling interval: 6655ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.37m    40.91s    3.32m    64.86%
        Req/Sec   150.23    107.63   536.00     73.58%
      540266 requests in 5.01m, 112.32MB read
      Socket errors: connect 237, read 0, write 26, timeout 26620
    Requests/sec:   1799.00
    Transfer/sec:    382.99KB


With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8004/index
    Running 30s test @ http://192.168.2.100:8004/index
      10 threads and 10 connections
      Thread calibration: mean lat.: 27.787ms, rate sampling interval: 157ms
      Thread calibration: mean lat.: 26.242ms, rate sampling interval: 171ms
      Thread calibration: mean lat.: 17.066ms, rate sampling interval: 14ms
      Thread calibration: mean lat.: 23.191ms, rate sampling interval: 157ms
      Thread calibration: mean lat.: 18.988ms, rate sampling interval: 17ms
      Thread calibration: mean lat.: 23.611ms, rate sampling interval: 20ms
      Thread calibration: mean lat.: 19.913ms, rate sampling interval: 21ms
      Thread calibration: mean lat.: 25.307ms, rate sampling interval: 159ms
      Thread calibration: mean lat.: 27.543ms, rate sampling interval: 154ms
      Thread calibration: mean lat.: 23.059ms, rate sampling interval: 150ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     3.05ms    1.53ms   8.38ms   73.71%
        Req/Sec     0.98      7.09    76.00     98.52%
      310 requests in 30.00s, 66.00KB read
    Requests/sec:     10.33
    Transfer/sec:      2.20KB

Simple query in DB with SQL
===========================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8004/agents
    Running 30s test @ http://127.0.0.1:8004/agents
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   324.59ms    1.15s   26.43s    99.07%
        Req/Sec    54.87     31.80   140.00     57.63%
      17498 requests in 30.02s, 121.85MB read
      Socket errors: connect 0, read 130, write 0, timeout 2388
    Requests/sec:    582.93
    Transfer/sec:      4.06MB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8004/agents
    Running 5m test @ http://192.168.2.100:8004/agents
      12 threads and 400 connections
      Thread calibration: mean lat.: 3208.406ms, rate sampling interval: 11935ms
      Thread calibration: mean lat.: 3700.374ms, rate sampling interval: 12779ms
      Thread calibration: mean lat.: 3268.693ms, rate sampling interval: 11649ms
      Thread calibration: mean lat.: 3237.077ms, rate sampling interval: 11157ms
      Thread calibration: mean lat.: 3724.595ms, rate sampling interval: 12632ms
      Thread calibration: mean lat.: 3414.967ms, rate sampling interval: 11755ms
      Thread calibration: mean lat.: 3220.802ms, rate sampling interval: 11534ms
      Thread calibration: mean lat.: 3507.489ms, rate sampling interval: 12279ms
      Thread calibration: mean lat.: 3486.669ms, rate sampling interval: 11984ms
      Thread calibration: mean lat.: 3650.601ms, rate sampling interval: 12083ms
      Thread calibration: mean lat.: 3758.517ms, rate sampling interval: 14155ms
      Thread calibration: mean lat.: 3661.614ms, rate sampling interval: 12279ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     2.36m     1.37m    4.92m    55.35%
        Req/Sec    21.87     11.16    57.00     74.55%
      83428 requests in 5.00m, 580.97MB read
      Socket errors: connect 0, read 218, write 156, timeout 37106
    Requests/sec:    277.96
    Transfer/sec:      1.94MB


With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8004/agents
    Running 30s test @ http://192.168.2.100:8004/agents
      10 threads and 10 connections
      Thread calibration: mean lat.: 42.976ms, rate sampling interval: 198ms
      Thread calibration: mean lat.: 55.998ms, rate sampling interval: 193ms
      Thread calibration: mean lat.: 38.301ms, rate sampling interval: 52ms
      Thread calibration: mean lat.: 44.267ms, rate sampling interval: 198ms
      Thread calibration: mean lat.: 40.666ms, rate sampling interval: 178ms
      Thread calibration: mean lat.: 40.553ms, rate sampling interval: 193ms
      Thread calibration: mean lat.: 35.104ms, rate sampling interval: 55ms
      Thread calibration: mean lat.: 38.621ms, rate sampling interval: 54ms
      Thread calibration: mean lat.: 33.702ms, rate sampling interval: 50ms
      Thread calibration: mean lat.: 39.105ms, rate sampling interval: 47ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    19.36ms    3.71ms  27.22ms   62.00%
        Req/Sec     0.99      3.89    21.00     95.93%
      300 requests in 30.01s, 2.09MB read
    Requests/sec:     10.00
    Transfer/sec:     71.29KB

Simple query in DB with Django ORM
==================================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8004/agents_with_orm
    Running 30s test @ http://127.0.0.1:8004/agents_with_orm
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   572.84ms    1.44s   13.33s    95.09%
        Req/Sec    66.34     38.74   142.00     58.87%
      17173 requests in 30.02s, 182.28MB read
      Socket errors: connect 0, read 77, write 0, timeout 2721
    Requests/sec:    572.13
    Transfer/sec:      6.07MB

