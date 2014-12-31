import asyncio
import logging
import os
import socket
from lockfile.pidlockfile import PIDLockFile
from .utils import STOP_SIGNALS

__all__ = [
    'Arbiter',
    ]



LOG = logging.getLogger(__name__)

class Arbiter:

    def __init__(self, config, application, loop=None, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.config = config
        self._app = application
        if loop is None:
            self._loop = asyncio.get_event_loop()
        else:
            self._loop = loop

    def start(self):
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.config['main']['host'], int(self.config['main']['port'])))
        self._sock.listen(int(self.config['performance']['backlog']))
        self._sock.setblocking(False)

        self._loop.run_until_complete(self._loop.create_server(
            self._app.make_handler, sock=self._sock))

        # To stop properly the daemon
        for sig_num in STOP_SIGNALS:
            self._loop.add_signal_handler(sig_num, self._app.pre_stop)

        LOG.info('Starting daemon on %s:%s...', self.config['main']['host'], self.config['main']['port'])

        for idx in range(1, int(self.config['performance']['workers'])):
            pid = os.fork()
            if pid:
                with PIDLockFile('%s_%s' % (self.config['main']['pid'], idx), timeout=0):
                    self._loop.create_task(self._app.start())
                    self._loop.run_forever()
                break
        else:
            with PIDLockFile('%s_0' % self.config['main']['pid'], timeout=0):
                self._loop.create_task(self._app.start())
                self._loop.run_forever()