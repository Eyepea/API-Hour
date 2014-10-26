import logging
import asyncio
import socket
import os

from lockfile.pidlockfile import PIDLockFile
import api_hour
from api_hour.utils import STOP_SIGNALS, get_config

from {{cookiecutter.app_name}} import endpoints
from {{cookiecutter.app_name}}.stores.couchdb import CouchDB


LOG = logging.getLogger(__name__)


class App(api_hour.Application):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Stores initialisation
        self.stores = {'couchdb': CouchDB('http://127.0.0.1:5984')}
        # routes
        self.add_url(['GET', 'POST'], '/index', endpoints.index.index)

    @asyncio.coroutine
    def start(self):
        pass

    def stop(self):
        LOG.info('Stopping daemon...')
        self._loop.stop()

def main(cli_args):
    loop = asyncio.get_event_loop()

    config = get_config(vars(cli_args))

    application = App(hostname='{{cookiecutter.hostname}}', config=config, loop=loop,
              access_log_format=('%(p)s %(h)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'))

    api_hour.MultiProcess(config=config, application=application, loop=loop)