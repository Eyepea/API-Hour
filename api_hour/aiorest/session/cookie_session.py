"""Cookie based sessions."""
import asyncio
import time
import hmac
import hashlib

from .base import create_session_factory
from .interface import SessionIdStore, SessionBackendStore


__all__ = [
    'CookieSessionFactory',
    'SecureCookie',
    ]


def CookieSessionFactory(loads, dumps, secret_key, cookie_name,
                         session_max_age=None,
                         domain=None, max_age=None, path=None,
                         secure=None, httponly=None,
                         *, loop=None):
    sid_store = SecureCookie(secret_key, cookie_name,
                             session_max_age=session_max_age,
                             domain=domain, max_age=max_age,
                             path=path, secure=secure,
                             httponly=httponly)
    backend = ClientSideBackend(loads, dumps)
    return create_session_factory(session_id_store=sid_store,
                                  backend_store=backend,
                                  loop=loop)


class ClientSideBackend(SessionBackendStore):
    """Client-side backend.

    Stores session object in session_id.
    """

    def __init__(self, loads, dumps):
        self._loads = loads
        self._dumps = dumps

    @asyncio.coroutine
    def load_session_data(self, cookie_value):
        """Load session data from decoded and verified cookie value.

        Returns session dict or None and empty string as session id
        """
        try:
            return self._loads(cookie_value), ''
        except (TypeError, ValueError):
            # TODO: log warning
            pass
        return None, None

    @asyncio.coroutine
    def save_session_data(self, session):
        """Save session and return bytes value to be stored in cookie.
        """
        if not session:
            return
        return self._dumps(dict(session))


class SecureCookie(SessionIdStore):
    """Cookie-based session factory.

    Stores session in cookies.
    """

    def __init__(self, secret_key, cookie_name,
                 session_max_age=None,
                 domain=None, max_age=None, path=None,
                 secure=None, httponly=None):
        if isinstance(secret_key, str):
            secret_key = secret_key.encode('utf-8')
        self._secret_key = secret_key
        self._cookie_name = cookie_name
        self._cookie_params = dict(domain=domain,
                                   max_age=max_age,
                                   path=path,
                                   secure=secure,
                                   httponly=httponly)
        self.session_max_age = session_max_age

    def get_session_id(self, request):
        name = self._cookie_name
        raw_value = request.cookies.get(name)
        return self._decode_cookie(raw_value)

    def put_session_id(self, request, cookie_value):
        if cookie_value is None:
            request.response.del_cookie(self._cookie_name)
        else:
            raw_value = self._encode_cookie(cookie_value)
            request.response.set_cookie(self._cookie_name, raw_value,
                                        **self._cookie_params)

    def _encode_cookie(self, value):
        """Encode and sign cookie value.

        value argument must be str instance.
        """
        assert isinstance(value, str)
        name = self._cookie_name
        timestamp = str(int(time.time()))
        singature = self._get_signature(name, value, timestamp)
        return '|'.join((value, timestamp, singature))

    def _decode_cookie(self, value):
        """Decode and verify cookie value.

        value argument must be str.
        Returns decoded bytes value of cookie
        or None if value could not be decoded or verified.
        """
        if not value:
            return None
        parts = value.split('|')
        if len(parts) != 3:
            return None
        name = self._cookie_name
        value, timestamp, sign = parts

        if self.session_max_age is not None:
            if int(timestamp) < int(time.time()) - self.session_max_age:
                return None

        expected_sign = self._get_signature(name, value, timestamp)
        if not hmac.compare_digest(expected_sign, sign):
            # TODO: log warning
            return None
        return value

    def _get_signature(self, *parts):
        sign = hmac.new(self._secret_key, digestmod=hashlib.sha1)
        sign.update(('|'.join(parts)).encode('utf-8'))
        return sign.hexdigest()
