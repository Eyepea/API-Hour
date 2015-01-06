from pprint import pprint
import logging
import asyncio

LOG = logging.getLogger(__name__)

from api_hour.plugins.aiohttp import JSON


@asyncio.coroutine
def index(request):
    return JSON({
        'index': 'hello!'
    })