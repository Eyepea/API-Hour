Command line used to launch WSGI server
=======================================

::

    $ gunicorn -w 16 -b 0.0.0.0:8000 application:app

JSON Serialization only
=======================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8000/index
    Running 30s test @ http://127.0.0.1:8000/index
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    13.16s    10.67s   26.31s    35.30%
        Req/Sec   222.56    483.37     2.96k    88.31%
      79598 requests in 30.10s, 13.51MB read
      Socket errors: connect 393, read 0, write 0, timeout 4040
    Requests/sec:   2644.71
    Transfer/sec:    459.73KB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8000/index
    Running 5m test @ http://192.168.2.100:8000/index
      12 threads and 400 connections
      Thread calibration: mean lat.: 975.406ms, rate sampling interval: 5050ms
      Thread calibration: mean lat.: 1665.266ms, rate sampling interval: 7925ms
      Thread calibration: mean lat.: 1193.631ms, rate sampling interval: 7426ms
      Thread calibration: mean lat.: 1155.229ms, rate sampling interval: 7716ms
      Thread calibration: mean lat.: 1314.758ms, rate sampling interval: 7131ms
      Thread calibration: mean lat.: 1094.373ms, rate sampling interval: 6709ms
      Thread calibration: mean lat.: 1296.058ms, rate sampling interval: 5922ms
      Thread calibration: mean lat.: 1296.384ms, rate sampling interval: 8634ms
      Thread calibration: mean lat.: 967.480ms, rate sampling interval: 5332ms
      Thread calibration: mean lat.: 2021.743ms, rate sampling interval: 13074ms
      Thread calibration: mean lat.: 1810.579ms, rate sampling interval: 12435ms
      Thread calibration: mean lat.: 1100.596ms, rate sampling interval: 7385ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     0.87m     0.86m    4.47m    70.40%
        Req/Sec   228.00     63.76   487.00     74.73%
      814328 requests in 5.00m, 138.24MB read
      Socket errors: connect 28, read 29, write 136, timeout 26549
    Requests/sec:   2714.49
    Transfer/sec:    471.85KB


With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8000/index
    Running 30s test @ http://192.168.2.100:8000/index
      10 threads and 10 connections
      Thread calibration: mean lat.: 2.649ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.794ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 3.134ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 3.398ms, rate sampling interval: 11ms
      Thread calibration: mean lat.: 2.395ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.683ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.642ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.244ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.725ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.131ms, rate sampling interval: 10ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     2.35ms    0.94ms   6.50ms   72.11%
        Req/Sec     1.00     10.13   111.00     99.03%
      310 requests in 30.00s, 53.89KB read
    Requests/sec:     10.33
    Transfer/sec:      1.80KB

Simple query in DB
==================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8000/agents
    Running 30s test @ http://127.0.0.1:8000/agents
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency   619.86ms    2.17s   13.31s    96.53%
        Req/Sec    71.41     41.79   153.00     58.69%
      19035 requests in 30.02s, 131.83MB read
      Socket errors: connect 0, read 66, write 0, timeout 2919
    Requests/sec:    634.05
    Transfer/sec:      4.39MB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8000/agents
    Running 5m test @ http://192.168.2.100:8000/agents
      12 threads and 400 connections
      Thread calibration: mean lat.: 3534.055ms, rate sampling interval: 12189ms
      Thread calibration: mean lat.: 3075.304ms, rate sampling interval: 12181ms
      Thread calibration: mean lat.: 3355.138ms, rate sampling interval: 13377ms
      Thread calibration: mean lat.: 3698.279ms, rate sampling interval: 12894ms
      Thread calibration: mean lat.: 3457.958ms, rate sampling interval: 13000ms
      Thread calibration: mean lat.: 3064.107ms, rate sampling interval: 11509ms
      Thread calibration: mean lat.: 3303.256ms, rate sampling interval: 11624ms
      Thread calibration: mean lat.: 3173.896ms, rate sampling interval: 11051ms
      Thread calibration: mean lat.: 3459.823ms, rate sampling interval: 12312ms
      Thread calibration: mean lat.: 3125.943ms, rate sampling interval: 11468ms
      Thread calibration: mean lat.: 2645.681ms, rate sampling interval: 10551ms
      Thread calibration: mean lat.: 3811.425ms, rate sampling interval: 12697ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     2.28m     1.50m    4.97m    43.65%
        Req/Sec    23.73     19.99    72.00     59.72%
      91296 requests in 5.00m, 632.28MB read
      Socket errors: connect 0, read 128, write 185, timeout 40638
    Requests/sec:    304.10
    Transfer/sec:      2.11MB

With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8000/agents
    Running 30s test @ http://192.168.2.100:8000/agents
      10 threads and 10 connections
      Thread calibration: mean lat.: 20.311ms, rate sampling interval: 53ms
      Thread calibration: mean lat.: 19.421ms, rate sampling interval: 51ms
      Thread calibration: mean lat.: 20.606ms, rate sampling interval: 52ms
      Thread calibration: mean lat.: 26.144ms, rate sampling interval: 54ms
      Thread calibration: mean lat.: 21.885ms, rate sampling interval: 56ms
      Thread calibration: mean lat.: 20.714ms, rate sampling interval: 50ms
      Thread calibration: mean lat.: 21.888ms, rate sampling interval: 55ms
      Thread calibration: mean lat.: 20.929ms, rate sampling interval: 47ms
      Thread calibration: mean lat.: 23.599ms, rate sampling interval: 54ms
      Thread calibration: mean lat.: 22.686ms, rate sampling interval: 53ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    18.74ms    4.81ms  47.78ms   70.00%
        Req/Sec     0.99      4.20    21.00     94.74%
      300 requests in 30.01s, 2.08MB read
    Requests/sec:     10.00
    Transfer/sec:     70.90KB


Simple query in DB with connection pool
=======================================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8000/agents_with_pool
    Running 30s test @ http://127.0.0.1:8000/agents_with_pool
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    12.09s    11.67s   26.34s    20.52%
        Req/Sec   212.38    365.73     2.64k    88.80%
      76412 requests in 30.14s, 36.35MB read
      Socket errors: connect 199, read 62, write 0, timeout 3505
      Non-2xx or 3xx responses: 75932
    Requests/sec:   2535.06
    Transfer/sec:      1.21MB

