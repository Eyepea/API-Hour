import aiohttp


class HttpCorsOptions(aiohttp.HttpException):
    """Http exception to handle CORS preflight requests.

    Raised in RESTServer.dispatch.
    """
    code = 200

    def __init__(self, headers):
        self.headers = headers
