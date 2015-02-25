import asyncio

from api_hour.plugins.aiohttp import JSON

from .. import services


@asyncio.coroutine
def agents(request):
    return JSON((yield from services.agents.list(request.app['ah_container'])))