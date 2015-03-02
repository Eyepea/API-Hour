from aiohttp.web import Response

try:
    import ujson as json
except ImportError:
    import json


class JSON(Response):
    """Serialize response to JSON with aiohttp.web"""

    def __init__(self, data, status=200,
                 reason=None, headers=None):
        body = json.dumps(data).encode('utf-8')

        super().__init__(body=body, status=status, reason=reason,
                         headers=headers, content_type='application/json')


class HTML(Response):
    """Serialize response to HTML with aiohttp.web"""

    def __init__(self, data, status=200,
                 reason=None, headers=None):

        body = data.encode('utf-8')

        super().__init__(body=body, status=status, reason=reason,
                         headers=headers, content_type='text/html')