import json
import mimetypes


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
        return json.dumps(self.data).encode(self.encoding)


class Html(Base):
    def serialize(self, request):
        request.response.headers.add('Content-Type', 'text/html')
        return self.data.encode(self.encoding)


class Asset(Base):
    def serialize(self, request):
        content_type = self.kwargs.get('content_type',
                                       mimetypes.guess_type(request.path)[0])
        request.response.headers.add('Content-Type', content_type)
        return self.data
