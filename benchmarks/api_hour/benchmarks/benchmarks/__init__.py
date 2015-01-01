import logging
import asyncio

import aiopg
import psycopg2.extras

import api_hour
import api_hour.aiorest

from . import endpoints


LOG = logging.getLogger(__name__)


class Container(api_hour.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Servers
        self.servers['http'] = api_hour.aiorest.Application(*args, **kwargs)
        self.servers['http'].ah_container = self # keep a reference to Container
        # routes
        self.servers['http'].add_url(['GET', 'POST'], '/index', endpoints.index.index)
        self.servers['http'].add_url('GET', '/agents_with_psycopg2_sync', endpoints.benchmarks.agents_with_psycopg2_sync)
        self.servers['http'].add_url('GET', '/agents_with_psycopg2_async', endpoints.benchmarks.agents_with_psycopg2_async)
        self.servers['http'].add_url('GET', '/agents_with_psycopg2_async_pool', endpoints.benchmarks.agents_with_psycopg2_async_pool)

    def make_servers(self):
        return [self.servers['http'].make_handler]

    @asyncio.coroutine
    def start(self):
        yield from super().start()
        # Add your custom start here, example with PostgreSQL:
        self.engines['pg'] = yield from aiopg.create_pool(host=self.config['engines']['pg']['host'],
                                                          port=int(self.config['engines']['pg']['port']),
                                                          dbname=self.config['engines']['pg']['dbname'],
                                                          user=self.config['engines']['pg']['user'],
                                                          password=self.config['engines']['pg']['password'],
                                                          cursor_factory=psycopg2.extras.RealDictCursor,
                                                          minsize=int(self.config['engines']['pg']['minsize']),
                                                          maxsize=int(self.config['engines']['pg']['maxsize']),
                                                          loop=self.loop)

    @asyncio.coroutine
    def stop(self):
        # Add your custom end here, example with PostgreSQL:
        if 'pg' in self.engines:
            self.engines['pg'].clear()
        yield from super().stop()