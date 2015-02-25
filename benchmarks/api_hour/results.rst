Command line used to launch API-Hour server
===========================================

::

    $ api_hour -ac benchmarks:Container

JSON Serialization only
=======================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8008/index
    Running 30s test @ http://127.0.0.1:8008/index
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    30.31ms   10.54ms 105.19ms   75.75%
        Req/Sec     1.11k   110.59     1.49k    75.54%
      395847 requests in 29.99s, 69.46MB read
    Requests/sec:  13200.94
    Transfer/sec:      2.32MB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8008/index
    Running 5m test @ http://192.168.2.100:8008/index
      12 threads and 400 connections
      Thread calibration: mean lat.: 1.867ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.860ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.885ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.896ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.876ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.805ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.845ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.909ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.890ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.835ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.830ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 1.831ms, rate sampling interval: 10ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.76ms    2.73ms  71.42ms   98.18%
        Req/Sec   350.95    118.15     1.67k    62.42%
      1198648 requests in 5.00m, 210.33MB read
    Requests/sec:   3995.59
    Transfer/sec:    717.96KB


With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8008/index
    Running 30s test @ http://192.168.2.100:8008/index
      10 threads and 10 connections
      Thread calibration: mean lat.: 2.992ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 3.050ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.603ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.769ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.704ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.390ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 3.093ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.655ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.238ms, rate sampling interval: 10ms
      Thread calibration: mean lat.: 2.367ms, rate sampling interval: 10ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     1.83ms  569.72us   3.50ms   68.95%
        Req/Sec     1.00     10.18   111.00     99.04%
      310 requests in 30.00s, 55.70KB read
    Requests/sec:     10.33
    Transfer/sec:      1.86KB


Simple query in DB
==================

Directly via localhost
----------------------

::

    $ wrk -t12 -c400 -d30s http://127.0.0.1:8008/agents
    Running 30s test @ http://127.0.0.1:8008/agents
      12 threads and 400 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    98.31ms   49.94ms 369.10ms   66.34%
        Req/Sec   346.76     62.13   646.00     73.31%
      125402 requests in 30.00s, 785.72MB read
    Requests/sec:   4179.54
    Transfer/sec:     26.19MB

Via 1Gb/s network
-----------------

With 4000 req/s
'''''''''''''''

::

    $ wrk2 -t12 -c400 -d5m -R 4000 http://192.168.2.100:8008/agents
    Running 5m test @ http://192.168.2.100:8008/agents
      12 threads and 400 connections
      Thread calibration: mean lat.: 102.329ms, rate sampling interval: 605ms
      Thread calibration: mean lat.: 92.505ms, rate sampling interval: 556ms
      Thread calibration: mean lat.: 89.615ms, rate sampling interval: 570ms
      Thread calibration: mean lat.: 152.949ms, rate sampling interval: 798ms
      Thread calibration: mean lat.: 124.916ms, rate sampling interval: 720ms
      Thread calibration: mean lat.: 127.807ms, rate sampling interval: 759ms
      Thread calibration: mean lat.: 69.161ms, rate sampling interval: 414ms
      Thread calibration: mean lat.: 120.730ms, rate sampling interval: 706ms
      Thread calibration: mean lat.: 136.565ms, rate sampling interval: 744ms
      Thread calibration: mean lat.: 91.879ms, rate sampling interval: 526ms
      Thread calibration: mean lat.: 152.116ms, rate sampling interval: 848ms
      Thread calibration: mean lat.: 109.957ms, rate sampling interval: 639ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     7.84s    17.70s    1.77m    89.23%
        Req/Sec   309.08     19.05   386.00     70.49%
      1109453 requests in 5.00m, 6.79GB read
    Requests/sec:   3698.21
    Transfer/sec:     23.17MB

With 10 req/s
'''''''''''''

::

    $ wrk2 -t10 -c10 -d30s -R 10 http://192.168.2.100:8008/agents
    Running 30s test @ http://192.168.2.100:8008/agents
      10 threads and 10 connections
      Thread calibration: mean lat.: 7.455ms, rate sampling interval: 21ms
      Thread calibration: mean lat.: 6.869ms, rate sampling interval: 19ms
      Thread calibration: mean lat.: 7.453ms, rate sampling interval: 24ms
      Thread calibration: mean lat.: 6.898ms, rate sampling interval: 21ms
      Thread calibration: mean lat.: 6.478ms, rate sampling interval: 24ms
      Thread calibration: mean lat.: 7.192ms, rate sampling interval: 20ms
      Thread calibration: mean lat.: 6.549ms, rate sampling interval: 20ms
      Thread calibration: mean lat.: 6.616ms, rate sampling interval: 18ms
      Thread calibration: mean lat.: 7.208ms, rate sampling interval: 20ms
      Thread calibration: mean lat.: 6.311ms, rate sampling interval: 17ms
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency     6.42ms    2.99ms  14.70ms   61.00%
        Req/Sec     1.02      7.10    62.00     97.97%
      301 requests in 30.01s, 1.89MB read
    Requests/sec:     10.03
    Transfer/sec:     64.36KB

