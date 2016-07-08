import logging

import api_hour
import aiohttp.web
from aiohttp.web import Response

logging.basicConfig(level=logging.INFO)  # enable logging for api_hour


class Container(api_hour.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Declare HTTP server
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http'].ah_container = self  # keep a reference in HTTP server to Container

        # Define HTTP routes
        self.servers['http'].router.add_route('GET',
                                              '/',
                                              self.index)

    # A HTTP handler example
    # More documentation: http://aiohttp.readthedocs.org/en/latest/web.html#handler
    async def index(self, request):
        message = 'Hello World !'
        return Response(text=message)


    # Container methods
    async def start(self):
        # A coroutine called when the Container is started
        await super().start()


    async def stop(self):
        # A coroutine called when the Container is stopped
        await super().stop()


    def make_servers(self):
        # This method is used by api_hour command line to bind your HTTP server on socket
        return [self.servers['http'].make_handler(logger=self.worker.log,
                                                  keep_alive=self.worker.cfg.keepalive,
                                                  access_log=self.worker.log.access_log,
                                                  access_log_format=self.worker.cfg.access_log_format)]
