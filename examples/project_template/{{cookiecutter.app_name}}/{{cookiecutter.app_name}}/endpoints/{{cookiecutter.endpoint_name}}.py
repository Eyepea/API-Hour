from pprint import pprint
import logging
import asyncio

LOG = logging.getLogger(__name__)


@asyncio.coroutine
def {{cookiecutter.endpoint_name}}(request):
    return {
        'index': 'hello!'
    }