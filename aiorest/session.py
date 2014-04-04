import asyncio
from datetime import datetime
from collections import MutableMapping


class Session(MutableMapping):
    """Session dict-like object.
    """

    def __init__(self, data=None, *, storage_save):
        self._storage_save = storage_save
        self._changed = False
        self._mapping = {}
        if data is not None:
            self._mapping.update(data)

    @property
    def created(self):
        return datetime.datetime.now()

    def changed(self):
        self._changed = True

    def invalidate(self):
        self._changed = True
        self._mapping = {}

    def save(self):
        return self._storage_save(self)

    def get_csrf_token(self):
        return "current_csrf_tocken or create new if not exists"

    def new_csrf_token(self):
        return 'new_csrf_token'

    def __len__(self):
        return len(self._mapping)

    def __iter__(self):
        return iter(self._mapping)

    def __contains__(self, key):
        return key in self._mapping

    def __getitem__(self, key):
        return self._mapping[key]

    def __setitem__(self, key, value):
        self._mapping[key] = value
        self._changed = True

    def __delitem__(self, key):
        del self._mapping[key]
        self._changed = True


class CookieSessionFactory:
    """Cookie-based session factory.
    """

    def __init__(self, dumps, loads, cookie_name='aiorest_sess', secret='secret'):
        self._cookie_name = cookie_name
        self._secret = secret
        self._dumps = dumps
        self._loads = loads

    @asyncio.coroutine
    def __call__(self, request):
        storage = CookieStorage(self._dumps, self._loads,
                                self._cookie_name, request)
        data = storage.load()
        return Session(data, storage_save=storage.save)
        yield


class CookieStorage:
    """Cookie storage.
    """

    def __init__(self, dumps, loads, cookie_name, request):
        self._dumps = dumps
        self._loads = loads
        self._cookie_name = cookie_name
        self._request = request

    def load(self):
        packed = self._request.cookies.get(self._cookie_name)
        if packed is not None:
            try:
                data = self._loads(packed)
            except (TypeError, ValueError):
                pass
            else:
                return data

    @asyncio.coroutine
    def save(self, session):
        return
        yield
