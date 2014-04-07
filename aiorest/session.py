import asyncio
from datetime import datetime
from collections import MutableMapping


class Session(MutableMapping):
    """Session dict-like object.
    """

    def __init__(self, data=None):
        self._changed = False
        self._mapping = {}
        if data is not None:
            self._mapping.update(data)

    @property
    def created(self):
        # TODO: implement
        return datetime.datetime.now()

    def changed(self):
        self._changed = True

    def invalidate(self):
        self._changed = True
        self._mapping = {}

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

    def __init__(self, dumps, loads, cookie_name, *, loop=None):
        self._dumps = dumps
        self._loads = loads
        self._cookie_name = cookie_name
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop

    def __call__(self, request, future):
        sess = Session(self._load_data(request))
        # FIXME: there may be the following issue:
        #   yield from request.session  # (response callback added)
        #   request.add_response_callback(modify_session)
        # this will cause session to be invalid
        request.add_response_callback(self._save, session=sess)
        future.set_result(sess)

    def _load_data(self, request):
        packed = request.cookies.get(self._cookie_name)
        if packed is not None:
            try:
                data = self._loads(packed)
            except (TypeError, ValueError):
                pass
            else:
                return data

    @asyncio.coroutine
    def _save(self, request, session):
        if session._changed:
            data = self._dumps(dict(session))
            request.response.set_cookie(self._cookie_name, data)
