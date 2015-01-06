import multiprocessing
import os

workers = 1

bind = "0.0.0.0:8008"
keepalive = 15
pidfile = '/run/lock/http_and_ssh.pid'
backlog = 10240000