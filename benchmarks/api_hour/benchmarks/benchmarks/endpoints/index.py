from pprint import pprint
import logging

LOG = logging.getLogger(__name__)

from api_hour.plugins.aiohttp import JSON


async def index(request):
    return JSON({'hello': 'world'})