import asyncio
import uuid
import pickle

from functools import partial

from .base import create_session_factory
from .cookie_session import SecureCookie, SessionBackendStore


__all__ = [
    'RedisBackend',
    'RedisSessionFactory',
    ]


_loads = partial(pickle.loads)
_dumps = partial(pickle.dumps, protocol=pickle.HIGHEST_PROTOCOL)


def RedisSessionFactory(redis, secret_key, cookie_name, *,
                        loads=_loads, dumps=_dumps, key_prefix='session:',
                        session_max_age=None, loop=None, **kwargs):
    cookie_store = SecureCookie(secret_key, cookie_name,
                                session_max_age=session_max_age,
                                **kwargs)
    backend = RedisBackend(redis, loads=loads, dumps=dumps,
                           session_max_age=session_max_age)
    return create_session_factory(session_id_store=cookie_store,
                                  backend_store=backend,
                                  loop=loop)


class RedisBackend(SessionBackendStore):
    """Redis session store backend.
    """

    def __init__(self, redis, *, loads=_loads, dumps=_dumps,
                 key_prefix='session:', session_max_age=None):
        self._redis = redis
        self._loads = loads
        self._dumps = dumps
        self._key_prefix = key_prefix
        self.session_max_age = session_max_age

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
