# -*- coding: utf-8 -
#
# This file is part of API-Hour, forked from gunicorn.workers._gaiohttp.py released under the MIT license.
# See the NOTICE for more information.

import asyncio
import os
import gunicorn.workers.base as base


class Worker(base.Worker):

    def __init__(self, *args, **kw):  # pragma: no cover
        super().__init__(*args, **kw)

        self.servers = []
        self.connections = {}

    def init_process(self):
        # create new event_loop after fork
        asyncio.get_event_loop().close()

        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

        super().init_process()

    def run(self):
        self._runner = asyncio.async(self._run(), loop=self.loop)

        try:
            self.loop.run_until_complete(self._runner)
        finally:
            self.loop.close()

    def wrap_protocol(self, proto):
        proto.connection_made = _wrp(
            proto, proto.connection_made, self.connections)
        proto.connection_lost = _wrp(
            proto, proto.connection_lost, self.connections, False)
        return proto

    @asyncio.coroutine
    def close(self):
        try:
            if hasattr(self.wsgi, 'close'):
                yield from self.wsgi.close()
        except:
            self.log.exception('Process shutdown exception')

    @asyncio.coroutine
    def _run(self):
        api_hour_app = self.app.callable(config=self.app.config, loop=self.loop)
        handlers = api_hour_app.make_servers()
        for i, sock in enumerate(self.sockets):
            if len(handlers) == 1:
                handler = handlers[0]
            else:
                handler = handlers[i]

            self.servers.append(
                (yield from self.loop.create_server(handler, sock=sock.sock)))
        yield from api_hour_app.start()

        # If our parent changed then we shut down.
        pid = os.getpid()
        try:
            while self.alive or self.connections:
                self.notify()

                if (self.alive and
                        pid == os.getpid() and self.ppid != os.getppid()):
                    self.log.info("Parent changed, shutting down: %s", self)
                    self.alive = False

                # stop accepting requests
                if not self.alive:
                    if self.servers:
                        self.log.info(
                            "Stopping server: %s, connections: %s",
                            pid, len(self.connections))
                        for server in self.servers:
                            server.close()
                        self.servers.clear()

                    # prepare connections for closing
                    for conn in self.connections.values():
                        if hasattr(conn, 'closing'):
                            conn.closing()

                yield from asyncio.sleep(1.0, loop=self.loop)
        except KeyboardInterrupt:
            pass

        if self.servers:
            yield from api_hour_app.stop()
            for server in self.servers:
                server.close()

        yield from self.close()


class _wrp:

    def __init__(self, proto, meth, tracking, add=True):
        self._proto = proto
        self._id = id(proto)
        self._meth = meth
        self._tracking = tracking
        self._add = add

    def __call__(self, *args):
        if self._add:
            self._tracking[self._id] = self._proto
        elif self._id in self._tracking:
            del self._tracking[self._id]

        conn = self._meth(*args)
        return conn
