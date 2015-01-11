# This file is part of API-Hour, forked from aiohttp/worker.py.
__all__ = ['Worker']

import asyncio
import os
import signal
import sys
import gunicorn.workers.base as base


class Worker(base.Worker):

    def __init__(self, *args, **kw):  # pragma: no cover
        super().__init__(*args, **kw)

        self.servers = {}
        self.exit_code = 0
        self.container = None

    def init_process(self):
        # create new event_loop after fork
        asyncio.get_event_loop().close()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        super().init_process()

    def run(self):
        self._runner = asyncio.async(self._run(), loop=self.loop)

        # prof = cProfile.Profile()
        # prof.enable()
        try:
            self.loop.run_until_complete(self._runner)
        finally:
            self.loop.close()
        # prof.disable()
        # prof.dump_stats('/tmp/out.pyprof')

        sys.exit(self.exit_code)

    @asyncio.coroutine
    def close(self):
        if self.servers:
            servers = self.servers
            self.servers = None

            # stop accepting connections
            for server, handler in servers.items():
                if hasattr(handler, 'connections'):
                    self.log.info("Stopping server: %s, connections: %s",
                                  self.pid, len(handler.connections))
                else:
                    self.log.info("Stopping server: %s",
                                  self.pid)
                server.close()

            # stop alive connections
            tasks = []
            for handler in servers.values():
                if hasattr(handler, 'finish_connections'):
                    tasks.append(handler.finish_connections(
                    timeout=self.cfg.graceful_timeout / 100 * 80))
            yield from asyncio.wait(tasks, loop=self.loop)

            # stop container
            yield from self.container.stop()

    @asyncio.coroutine
    def _run(self):
        self.container = self.app.callable(config=self.app.config,
                                           worker=self,
                                           loop=self.loop)
        handlers = self.container.make_servers()
        for i, sock in enumerate(self.sockets):
            if len(handlers) == 1:
                handler = handlers[0]
            else:
                handler = handlers[i]

            srv = yield from self.loop.create_server(handler, sock=sock.sock) # @todo: add unix socket support
            self.servers[srv] = handler
        yield from self.container.start()

        # If our parent changed then we shut down.
        pid = os.getpid()
        try:
            while self.alive:
                self.notify()

                if pid == os.getpid() and self.ppid != os.getppid():
                    self.alive = False
                    self.log.info("Parent changed, shutting down: %s", self)
                else:
                    yield from asyncio.sleep(1.0, loop=self.loop)
        except (Exception, BaseException, GeneratorExit, KeyboardInterrupt):
            pass

        yield from self.close()

    def init_signal(self):
        # init new signaling
        self.loop.add_signal_handler(signal.SIGQUIT, self.handle_quit)
        self.loop.add_signal_handler(signal.SIGTERM, self.handle_exit)
        self.loop.add_signal_handler(signal.SIGINT, self.handle_quit)
        self.loop.add_signal_handler(signal.SIGWINCH, self.handle_winch)
        self.loop.add_signal_handler(signal.SIGUSR1, self.handle_usr1)
        self.loop.add_signal_handler(signal.SIGABRT, self.handle_abort)

        # Don't let SIGTERM and SIGUSR1 disturb active requests
        # by interrupting system calls
        signal.siginterrupt(signal.SIGTERM, False)
        signal.siginterrupt(signal.SIGUSR1, False)

    def handle_quit(self, sig, frame):
        self.alive = False

    def handle_abort(self, sig, frame):
        self.alive = False
        self.exit_code = 1