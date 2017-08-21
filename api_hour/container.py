from abc import abstractmethod
import asyncio
from collections import OrderedDict
import logging



__all__ = [
    'Container',
]

LOG = logging.getLogger(__name__)


class Container:

    def __init__(self, config, worker, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        super().__init__()
        self.config = config
        self.worker = worker
        # Engines initialisation
        self.engines = {}
        # Services initialisation
        self.services = {}
        self.servers = OrderedDict()
        self._stopping = False

    @abstractmethod
    async def make_servers(self, sockets):
        """Return handlers to serve data"""

    @classmethod
    def make_event_loop(cls, config):
        """To customize loop generation"""
        return asyncio.new_event_loop()

    async def pre_start(self):
        pass

    async def start(self):
        LOG.info('Starting application...')

    def pre_stop(self):
        if not self._stopping:
            self._stopping = True
            task = asyncio.ensure_future(self.shutdown(), loop=self.loop)
            task.add_done_callback(self.cleanup())
        else:
            LOG.debug('Already stopping application, not doing anything')

    async def shutdown(self):
        pass

    async def cleanup(self):
        pass

    def post_stop(self, future):
        pass
