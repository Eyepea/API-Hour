from pprint import pprint
import logging
import asyncio

LOG = logging.getLogger(__name__)


@asyncio.coroutine
def index(request):
    return {
        'index': 'hello!'
    }