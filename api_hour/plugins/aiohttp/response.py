from aiohttp.web import HTTPException

try:
    import ujson as json
except ImportError:
    import json


class JSON(HTTPException):
    """Serialize response to JSON with aiohttp.web"""

    def __init__(self, data, status=200,
                 reason=None, headers=None):
        body = json.dumps(data).encode('utf-8')
        self.status_code = status

        super().__init__(body=body, reason=reason,
                         headers=headers, content_type='application/json')


class HTML(HTTPException):
    """Serialize response to HTML with aiohttp.web"""

    def __init__(self, data, status=200,
                 reason=None, headers=None):
        body = data.encode('utf-8')
        self.status_code = status

        super().__init__(body=body, reason=reason,
                         headers=headers, content_type='text/html')
