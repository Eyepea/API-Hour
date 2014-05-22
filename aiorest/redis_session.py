import asyncio
import uuid
import pickle

from functools import partial

from .session import BaseSessionFactory


_loads = partial(pickle.loads)
_dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)


class RedisSessionFactory(BaseSessionFactory):
    """Redis-based session storage.
    """

    def __init__(self, redis, secret_key, cookie_name, *,
                 loads=_loads, dumps=_dumps, key_prefix='session:',
                 loop=None, **kwargs):
        super().__init__(secret_key, cookie_name, loop=loop, **kwargs)
        if loop is None:
            loop = asyncio.get_event_loop()
        self._redis = redis
        self._loads = loads
        self._dumps = dumps
        self._key_prefix = key_prefix
        self._loop = loop
        assert callable(loads), "loads argument must be callable"
        assert callable(dumps), "dumps argument must be callable"

    @asyncio.coroutine
    def load_session_data(self, cookie_value):
        """Loads session data pointed by sid stored in cookies.
        """
        sid = cookie_value
        key = self._make_key(sid)
        packed = yield from self._redis.get(key)
        if packed is not None:
            try:
                data = self._loads(packed)
            except (TypeError, ValueError):
                pass
            else:
                return data, sid
        return None, None

    @asyncio.coroutine
    def save_session_data(self, session):
        """Saves session data in redis and returns sid.
        """
        if session.new:
            sid = self.new_sid()
        else:
            sid = session.identity
        key = self._make_key(sid)
        if not session and sid:
            yield from self._redis.delete([key])
            return None
        data = self._dumps(dict(session))
        if self.session_max_age is not None:
            yield from self._redis.setex(key, self.session_max_age, data)
        else:
            yield from self._redis.set(key, data)
        return sid

    def new_sid(self):
        """Returns new sid.
        """
        return uuid.uuid4().hex

    def _make_key(self, sid):
        return '{prefix}{sid}'.format(
            prefix=self._key_prefix, sid=sid).encode('utf-8')
