import asyncio
import hmac
import hashlib
import time
from collections import MutableMapping


class Session(MutableMapping):
    """Session dict-like object.
    """

    def __init__(self, data=None, new=False):
        self._changed = False
        self._mapping = {}
        self._new = new
        if data is not None:
            self._mapping.update(data)

    @property
    def new(self):
        return self._new

    def changed(self):
        self._changed = True

    def invalidate(self):
        self._changed = True
        self._mapping = {}

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


class BaseSessionFactory:

    def __init__(self, secret_key, cookie_name, 
                 session_max_age=None,
                 domain=None, max_age=None, path=None,
                 secure=None, httponly=None, *,
                 loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._secret_key = secret_key
        self._cookie_name = cookie_name
        self._session_max_age = session_max_age
        self._cookie_params = dict(domain=domain,
                                   max_age=max_age,
                                   path=path,
                                   secure=secure,
                                   httponly=httponly)
        self._loop = loop

    def __call__(self, request, fut):
        """Instantiate Session object.
        """
        asyncio.Task(self._load(request, fut), loop=self._loop)

    @asyncio.coroutine
    def _load(self, request, fut):
        """Load or creates new session.
        """
        name = self._cookie_name
        raw_value = request.cookies.get(name)
        try:
            cookie_value = self._decode_cookie(raw_value)
            if cookie_value is None:
                sess = Session(new=True)
            else:
                data = yield from self.load_session_data(cookie_value)
                sess = Session(data, new=(data is None))
        except Exception as exc:
            fut.set_exception(exc)
        else:
            fut.set_result(sess)
            # FIXME: the next line is a subject to the following issue:
            #   yield from request.session  # (response callback added)
            #   request.add_response_callback(modify_session)
            # this will cause session to be invalid
            request.add_response_callback(self._save, session=sess)

    @asyncio.coroutine
    def _save(self, request, session):
        """Save session.
        """
        if not session._changed:
            return
        cookie_value = yield from self.save_session_data(session)
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

        if self._session_max_age is not None:
            if int(timestamp) < int(time.time()) - self._session_max_age:
                return None

        expected_sign = self._get_signature(name, value, timestamp)
        if not hmac.compare_digest(expected_sign, sign):
            # TODO: log warning
            return None
        try:
            return value
        except Exception:
            # TODO: log warning
            return None

    def _get_signature(self, *parts):
        sign = hmac.new(self._secret_key, digestmod=hashlib.sha1)
        sign.update(('|'.join(parts)).encode('utf-8'))
        return sign.hexdigest()

    @asyncio.coroutine
    def load_session_data(self, value):
        """Loads session data based on value of session cookie.

        Must be implemented in child class.
        Returns session dict or None
        """
        raise NotImplementedError

    @asyncio.coroutine
    def save_session_data(self, session):
        """Stores session data and returns session cookie value.

        Must be implemented in child class.
        Returns session cookie value or None if should be deleted.
        """
        raise NotImplementedError


class CookieSessionFactory(BaseSessionFactory):
    """Cookie-based session factory.

    Stores session in cookies.
    """

    def __init__(self, loads, dumps, *, loop=None, **kwargs):
        super().__init__(loop=loop, **kwargs)
        self._loads = loads
        self._dumps = dumps

    @asyncio.coroutine
    def load_session_data(self, cookie_value):
        """Load session data from decoded and verified cookie value.
        """
        try:
            return self._loads(cookie_value)
        except (TypeError, ValueError):
            pass
        return
        yield

    @asyncio.coroutine
    def save_session_data(self, session):
        """Save session and return bytes value to be stored in cookie.
        """
        if not session:
            return
        return self._dumps(dict(session))
        yield
