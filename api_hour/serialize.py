import ujson
import asyncio
import mimetypes
import functools


class Base:
    def __init__(self, data, *, encoding='utf-8', **kwargs):
        self.data = data
        self.kwargs = kwargs
        self.encoding = encoding

    def serialize(self, request):
        return self.data.encode(self.encoding)


class Json(Base):
    def serialize(self, request):
        request.response.headers.add('Content-Type', 'application/json')
        return ujson.dumps(self.data).encode(self.encoding)


class Html(Base):
    def serialize(self, request):
        request.response.headers.add('Content-Type', 'text/html')
        return self.data.encode(self.encoding)


class Asset(Base):
    def __init__(self, *args, content_type=None, **kwargs):
        self._content_type = content_type
        super().__init__(*args, **kwargs)

    def serialize(self, request):
        if self._content_type is None:
            content_type = self.kwargs.get('content_type',
                                           mimetypes.guess_type(request.path)[0])
            request.response.headers.add('Content-Type', content_type)
        return self.data


def to(serializer, **serializer_kwargs):
    serializer = serializer.title()
    serializer = globals()[serializer]

    def decorator(f):
        @functools.wraps(f)
        @asyncio.coroutine
        def wrapper(*args, **kwargs):
            content = f(*args, **kwargs)
            if asyncio.iscoroutine(content):
                content = (yield from content)
            return serializer(content, **serializer_kwargs)

        return wrapper

    return decorator
