import asyncio

from api_hour.plugins.aiohttp import JSON

from .. import services


async def agents(request):
    return JSON(await services.agents.list(request.app['ah_container']))