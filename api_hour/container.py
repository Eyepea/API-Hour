from abc import abstractmethod
import asyncio
from collections import OrderedDict
import logging


__all__ = [
    'Container',
]

LOG = logging.getLogger(__name__)


class Container:

    def __init__(self, config, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        super().__init__()
        self.config = config
        # engines initialisation
        self.engines = {}
        # Stores initialisation
        self.stores = {}
        self.servers = OrderedDict()
        self._stopping = False

    @abstractmethod
    def make_servers(self):
        """Return handlers to serve data"""

    @asyncio.coroutine
    def start(self):
        LOG.info('Starting application...')

    def pre_stop(self):
        if not self._stopping:
            self._stopping = True
            task = self.loop.create_task(self.stop())
            task.add_done_callback(self.post_stop)
        else:
            LOG.debug('Already stopping application, not doing anything')

    @asyncio.coroutine
    def stop(self):
        LOG.info('Stopping application...')

    def post_stop(self, future):
        pass
