
JSON Serialization only
=======================

$ wrk -t12 -c400 -d30s http://localhost:5050/hello
Running 30s test @ http://localhost:5050/hello
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency    16.29ms   37.37ms 827.95ms   99.22%
    Req/Sec   741.88    262.60     1.94k    70.61%
  262947 requests in 30.00s, 54.67MB read
  Socket errors: connect 0, read 262917, write 0, timeout 30
Requests/sec:   8764.77
Transfer/sec:      1.82MB


Simple query in DB
==================

With sync psycopg2
------------------

$ wrk -t12 -c400 -d30s http://127.0.0.1:5050/agents_with_psycopg2_sync
Running 30s test @ http://127.0.0.1:5050/agents_with_psycopg2_sync
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   386.44ms    1.75s   26.42s    98.76%
    Req/Sec    64.68     30.33   163.00     67.28%
  17634 requests in 30.03s, 100.94MB read
  Socket errors: connect 0, read 17674, write 0, timeout 2465
Requests/sec:    587.31
Transfer/sec:      3.36MB

With aiopg
----------

$ wrk -t12 -c400 -d30s http://127.0.0.1:5050/agents_with_psycopg2_async
Running 30s test @ http://127.0.0.1:5050/agents_with_psycopg2_async
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   656.75ms    2.62s   26.71s    98.83%
    Req/Sec    48.31     17.45   104.00     74.68%
  15980 requests in 30.02s, 101.05MB read
  Socket errors: connect 0, read 15973, write 0, timeout 1471
Requests/sec:    532.35
Transfer/sec:      3.37MB

With aiopg and socket pool
--------------------------

$ wrk -t12 -c400 -d30s http://127.0.0.1:5050/agents_with_psycopg2_async_pool
Running 30s test @ http://127.0.0.1:5050/agents_with_psycopg2_async_pool
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   256.35ms    1.14s    6.62s    96.78%
    Req/Sec   264.27    119.07   750.00     69.44%
  93824 requests in 29.97s, 593.33MB read
  Socket errors: connect 0, read 93802, write 0, timeout 850
Requests/sec:   3130.86
Transfer/sec:     19.80M

With aiopg and socket pool and ujson
------------------------------------

$ wrk -t12 -c400 -d30s http://127.0.0.1:5050/agents_with_psycopg2_async_pool
Running 30s test @ http://127.0.0.1:5050/agents_with_psycopg2_async_pool
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   209.54ms    1.16s   13.14s    97.62%
    Req/Sec   291.70    113.84   804.00     73.83%
  104855 requests in 29.98s, 600.19MB read
  Socket errors: connect 0, read 104837, write 0, timeout 617
Requests/sec:   3498.03
Transfer/sec:     20.02MB
