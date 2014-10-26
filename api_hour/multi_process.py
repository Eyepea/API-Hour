import asyncio
import logging
import os
import socket
from lockfile.pidlockfile import PIDLockFile
from .utils import STOP_SIGNALS

__all__ = [
    'MultiProcess',
    ]



LOG = logging.getLogger(__name__)

class MultiProcess:

    def __init__(self, config, application, loop=None, *args, **kwargs):
        # super().__init__(*args, **kwargs)
        self.config = config
        if loop is None:
            self._loop = asyncio.get_event_loop()
        self._app = application
        self._sock = socket.socket()
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.config['main']['host'], int(self.config['main']['port'])))
        self._sock.listen(int(self.config['performance']['backlog']))
        self._sock.setblocking(False)

        loop.run_until_complete(loop.create_server(
            self._app.make_handler, sock=self._sock))

        # To stop properly the daemon
        for sig_num in STOP_SIGNALS:
            loop.add_signal_handler(sig_num, self._app.stop)

        LOG.info('Starting daemon on 0.0.0.0:5050...')

        for idx in range(1, int(config['performance']['workers'])):
            pid = os.fork()
            if pid:
                with PIDLockFile('%s_%s' % (config['main']['pid'], idx), timeout=0):
                    loop.create_task(self._app.start())
                    loop.run_forever()
                break
        else:
            with PIDLockFile('%s_0' %config['main']['pid'], timeout=0):
                loop.create_task(self._app.start())
                loop.run_forever()