from aiohttp.web import Response
import ujson

class JSON(Response):
    """Serialize response to JSON with aiohttp.web"""

    def __init__(self, json, status=200,
                 reason=None, headers=None):
        body = ujson.dumps(json).encode('utf-8')

        super().__init__(body=body, status=status, reason=reason,
                         headers=headers, content_type='application/json')