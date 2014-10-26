$ gunicorn -w 16 application:app

JSON Serialization only
=======================

$ wrk -t12 -c400 -d30s http://localhost:8000/hello
Running 30s test @ http://localhost:8000/hello
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency     1.08s   886.63ms   3.28s    78.01%
    Req/Sec   152.54    437.95     3.46k    90.91%
  60270 requests in 30.03s, 10.23MB read
  Socket errors: connect 396, read 0, write 0, timeout 4863
Requests/sec:   2006.82
Transfer/sec:    348.84KB


Simple query in DB
==================

$ wrk -t12 -c400 -d30s http://localhost:8000/agents
Running 30s test @ http://localhost:8000/agents
  12 threads and 400 connections
  Thread Stats   Avg      Stdev     Max   +/- Stdev
    Latency   838.99ms    3.78s   26.42s    97.62%
    Req/Sec    64.59     37.19   145.00     57.59%
  17172 requests in 30.01s, 108.04MB read
  Socket errors: connect 0, read 81, write 0, timeout 2547
Requests/sec:    572.23
Transfer/sec:      3.60MB
