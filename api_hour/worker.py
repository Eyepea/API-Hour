# This file is part of API-Hour, forked from aiohttp/worker.py.
__all__ = ['Worker']

import asyncio
import os
import signal
import sys
import gunicorn.workers.base as base

try:
    import aiohttp.web
except ImportError:
    aiohttp = None

# from pycallgraph import PyCallGraph
# from pycallgraph import Config
# from pycallgraph.output import GraphvizOutput


class Worker(base.Worker):

    def __init__(self, *args, **kw):  # pragma: no cover
        super().__init__(*args, **kw)

        self.handlers = {}
        self.exit_code = 0
        self.container = None
        self.loop = None

    def init_process(self):
        # create new event_loop after fork
        asyncio.get_event_loop().close()

        super().init_process()
        # graphviz = GraphvizOutput()
        # graphviz.output_file = '/tmp/test.png'
        #
        # with PyCallGraph(output=graphviz):
        #     super().init_process()

    def run(self):
        self.loop = self.app.callable.make_event_loop(config=self.app.config)
        asyncio.set_event_loop(self.loop)

        self._init_signals()

        self._runner = asyncio.ensure_future(self._run(), loop=self.loop)

        # import cProfile
        # prof = cProfile.Profile()
        # prof.enable()
        try:
            self.loop.run_until_complete(self._runner)
        finally:
            self.loop.close()
        # prof.disable()
        # prof.dump_stats('/tmp/out.pyprof')

        sys.exit(self.exit_code)

    async def close(self):
        if self.handlers:
            servers = self.handlers
            self.handlers = None

            # stop accepting connections
            self.log.info("Closing %s servers. PID: %s", len(servers), self.pid)
            closing = list()
            for server, handler in servers.items():
                server.close()
                closing.append(server.wait_closed())

            if closing:
                await asyncio.wait(closing, return_when=asyncio.ALL_COMPLETED, loop=self.loop)

            self.log.debug('Shutting down')
            await self.container.shutdown()
            tasks = []
            for handler in servers.values():
                if aiohttp and isinstance(handler, aiohttp.web.Server):
                    tasks.append(handler.shutdown(timeout=self.cfg.graceful_timeout / 100 * 80))
            if tasks:
                await asyncio.wait(tasks, loop=self.loop, return_when=asyncio.ALL_COMPLETED)

            self.log.debug('Cleaning container')
            await self.container.cleanup()

            self.log.debug('All server closed')

        else:
            await self.container.shutdown()
            await self.container.cleanup()

    async def _run(self):
        self.container = self.app.callable(config=self.app.config,
                                           worker=self,
                                           loop=self.loop)
        await self.container.pre_start()
        if asyncio.iscoroutinefunction(self.container.make_servers):
            self.handlers = await self.container.make_servers(self.sockets)
        else:
            handlers = self.container.make_servers()
            for i, sock in enumerate(self.sockets):
                if len(handlers) == 1:
                    handler = handlers[0]
                else:
                    handler = handlers[i]
                if asyncio.iscoroutinefunction(handler):
                    self.log.info('Handler "%s" is a coroutine => High-level AsyncIO API', handler)
                    srv = await asyncio.start_server(handler, sock=sock.sock, loop=self.loop)
                else:
                    self.log.info('Handler "%s" is a function => Low-level AsyncIO API', handler)
                    srv = await self.loop.create_server(handler, sock=sock.sock)
                self.handlers[srv] = handler
        await self.container.start()

        # If our parent changed then we shut down.
        pid = os.getpid()
        try:
            while self.alive:
                self.notify()

                if pid == os.getpid() and self.ppid != os.getppid():
                    self.alive = False
                    self.log.info("Parent changed, shutting down: %s", self)
                else:
                    await asyncio.sleep(1.0, loop=self.loop)
        except (Exception, BaseException, GeneratorExit, KeyboardInterrupt):
            pass

        await self.close()

    def init_signals(self):
        # init_signals initialized later in _init_signals because self.loop isn't initialized yet
        pass

    def _init_signals(self):
        # Set up signals through the event loop API.

        self.loop.add_signal_handler(signal.SIGQUIT, self.handle_quit,
                                     signal.SIGQUIT, None)

        self.loop.add_signal_handler(signal.SIGTERM, self.handle_exit,
                                     signal.SIGTERM, None)

        self.loop.add_signal_handler(signal.SIGINT, self.handle_quit,
                                     signal.SIGINT, None)

        self.loop.add_signal_handler(signal.SIGWINCH, self.handle_winch,
                                     signal.SIGWINCH, None)

        self.loop.add_signal_handler(signal.SIGUSR1, self.handle_usr1,
                                     signal.SIGUSR1, None)

        self.loop.add_signal_handler(signal.SIGABRT, self.handle_abort,
                                     signal.SIGABRT, None)

        # Don't let SIGTERM and SIGUSR1 disturb active requests
        # by interrupting system calls
        signal.siginterrupt(signal.SIGTERM, False)
        signal.siginterrupt(signal.SIGUSR1, False)

    def handle_quit(self, sig, frame):
        self.alive = False

    def handle_abort(self, sig, frame):
        self.alive = False
        self.exit_code = 1
