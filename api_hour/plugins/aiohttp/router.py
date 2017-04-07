from aiohttp.web_urldispatcher import UrlDispatcher


class Router(UrlDispatcher):
    def __init__(self, container):
        self._container = container
        self._container.env_config = dict()
        super().__init__()

    def add_route(self, method, path, handler,
                  *, name=None, expect_handler=None, env_config=None):
        resource = self.add_resource(path, name=name)
        if name:
            self._container.env_config[name] = env_config or []
        return resource.add_route(method, handler,
                                  expect_handler=expect_handler)
