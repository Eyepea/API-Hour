from pprint import pprint
import logging
import asyncio
from urllib.parse import parse_qsl

from aiohttp.multidict import MultiDict

LOG = logging.getLogger(__name__)


@asyncio.coroutine
def index(request):
    return {
        'index': 'hello!'
    }