
JSON Serialization only
=======================

$ wrk -t12 -c400 -d30s http://127.0.0.1:8008/index
Running 30s test @ http://127.0.0.1:8008/index
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    30.00ms    7.98ms 256.89ms   88.59%
    Req/Sec     1.12k   160.39     2.05k    78.41%
  396161 requests in 30.00s, 69.89MB read
Requests/sec:  13205.29
Transfer/sec:      2.33MB

Simple query in DB
==================

With sync psycopg2
------------------

$ wrk -t12 -c400 -d30s http://127.0.0.1:8008/agents_with_psycopg2_sync
Running 30s test @ http://127.0.0.1:8008/agents_with_psycopg2_sync
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   386.44ms    1.75s   26.42s    98.76%
    Req/Sec    64.68     30.33   163.00     67.28%
  17634 requests in 30.03s, 100.94MB read
  Socket errors: connect 0, read 17674, write 0, timeout 2465
Requests/sec:    587.31
Transfer/sec:      3.36MB

With aiopg and socket pool
--------------------------

$ wrk -t12 -c400 -d30s http://127.0.0.1:8008/agents_with_psycopg2_async_pool
Running 30s test @ http://127.0.0.1:8008/agents_with_psycopg2_async_pool
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    92.92ms   52.97ms 478.31ms   72.59%
    Req/Sec   356.84     45.66   528.00     76.43%
  128864 requests in 29.98s, 734.29MB read
Requests/sec:   4298.94
Transfer/sec:     24.50MB