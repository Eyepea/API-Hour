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

    def stop_daemon(self):
        LOG.info('Stopping daemon...')
        self._loop.stop()


def main(cli_args):
    loop = asyncio.get_event_loop()

    config = get_config(vars(cli_args))

    app = App(hostname='{{cookiecutter.hostname}}', config=config, loop=loop,
              access_log_format=('%(p)s %(h)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'))

    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 5050))
    sock.listen(102400)
    sock.setblocking(False)

    srv = loop.run_until_complete(loop.create_server(
        app.make_handler, sock=sock))

    # To stop the daemon properly
    for sig_num in STOP_SIGNALS:
        loop.add_signal_handler(sig_num, app.stop_daemon)

    LOG.info('Starting daemon on 0.0.0.0:5050...')

    for idx in range(1, int(config['performance']['workers'])):
        pid = os.fork()
        if pid:
            with PIDLockFile('%s_%s' % (config['main']['pid'], idx), timeout=0):
                loop.run_forever()
            break
    else:
        with PIDLockFile('%s_0' %config['main']['pid'], timeout=0):
            loop.run_forever()