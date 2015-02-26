import logging
import asyncio

import aiouv
import aiohttp.web
import aiopg
import psycopg2.extras

import api_hour

from . import endpoints


LOG = logging.getLogger(__name__)


class Container(api_hour.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.config is None:
            raise ValueError('An API-Hour config dir is needed.')
        ## Servers
        # You can define several servers, to listen HTTP and SSH for example.
        # If you do that, you need to listen on two ports with api_hour --bind command line.
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http']['ah_container'] = self  # keep a reference to Container
        # routes
        self.servers['http'].router.add_route('GET',
                                              '/index',
                                              endpoints.index.index)
        self.servers['http'].router.add_route('GET',
                                              '/agents',
                                              endpoints.benchmarks.agents)

    def make_servers(self):
        # This method is used by api_hour command line to bind each server on each socket
        # Please don't touch if you don't understand how it works
        return [self.servers['http'].make_handler(logger=self.worker.log,
                                                  debug=False,
                                                  keep_alive=self.worker.cfg.keepalive,
                                                  access_log=self.worker.log.access_log,
                                                  access_log_format=self.worker.cfg.access_log_format)]

    @classmethod
    def make_event_loop(cls, config):
        """To customize loop generation"""
        if config['event_loop'] == 'aiouv':
            LOG.info('Using aiouv event loop')
            return aiouv.EventLoop()
        else:
            LOG.info('Using default AsyncIO event loop')
            return asyncio.new_event_loop()

    @asyncio.coroutine
    def start(self):
        yield from super().start()
        LOG.info('Starting engines...')
        # Add your custom engines here, example with PostgreSQL:
        self.engines['pg'] = self.loop.create_task(aiopg.create_pool(host=self.config['engines']['pg']['host'],
                                                                     port=int(self.config['engines']['pg']['port']),
                                                                     sslmode='disable',
                                                                     dbname=self.config['engines']['pg']['dbname'],
                                                                     user=self.config['engines']['pg']['user'],
                                                                     password=self.config['engines']['pg']['password'],
                                                                     cursor_factory=psycopg2.extras.RealDictCursor,
                                                                     minsize=int(self.config['engines']['pg']['minsize']),
                                                                     maxsize=int(self.config['engines']['pg']['maxsize'])))
        yield from asyncio.wait([self.engines['pg']], return_when=asyncio.ALL_COMPLETED)

        LOG.info('All engines ready !')


    @asyncio.coroutine
    def stop(self):
        LOG.info('Stopping engines...')
        # Add your custom end here, example with PostgreSQL:
        if 'pg' in self.engines:
            if self.engines['pg'].done():
                self.engines['pg'].result().terminate()
                yield from self.engines['pg'].result().wait_closed()
            else:
                yield from self.engines['pg'].cancel()
        LOG.info('All engines stopped !')
        yield from super().stop()