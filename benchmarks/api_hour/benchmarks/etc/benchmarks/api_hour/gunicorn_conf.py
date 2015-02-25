import multiprocessing
import os

workers = multiprocessing.cpu_count() * 2
if os.environ.get('TRAVIS') == 'true':
    workers = 2

bind = "0.0.0.0:8008"
keepalive = 45
pidfile = '/run/lock/benchmarks.pid'
backlog = 10240000