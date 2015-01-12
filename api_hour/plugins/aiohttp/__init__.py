from aiohttp.web import Response

try:
    import ujson as json
except ImportError:
    import json

class JSON(Response):
    """Serialize response to JSON with aiohttp.web"""

    def __init__(self, json, status=200,
                 reason=None, headers=None):
        body = json.dumps(json).encode('utf-8')

        super().__init__(body=body, status=status, reason=reason,
                         headers=headers, content_type='application/json')