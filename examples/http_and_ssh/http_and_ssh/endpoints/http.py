from pprint import pprint
import logging
import asyncio

from api_hour.plugins.aiohttp import JSON

import http_and_ssh

LOG = logging.getLogger(__name__)

"""
You handle inputs with outside world here
"""

@asyncio.coroutine
def get_ssh_content(request):
    container = request.app.ah_container
    # return JSON({
    #     'current_ssh_text': container.current_ssh_text
    # })
    return JSON({
        'current_ssh_text': http_and_ssh.CURRENT_SSH_TEXT
    })

# Endpoint example with a Service

# from ..services.data import get_random_record
#
# @asyncio.coroutine
# def db(request):
#     """Test type 2: Single database query"""
#     container = request.app.ah_container
#
#     return JSON((yield from get_random_record(container)))
#
