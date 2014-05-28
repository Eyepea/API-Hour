import asyncio
from collections import MutableMapping

from .interface import SessionIdStore, SessionBackendStore

__all__ = ['Session', 'create_session_factory']


class Session(MutableMapping):
    """Session dict-like object.
    """

    def __init__(self, data=None, identity=None):
        self._changed = False
        self._mapping = {}
        self._identity = identity
        if data is not None:
            self._mapping.update(data)

    def __repr__(self):
        return '<{} [new:{}, changed:{}] {!r}>'.format(
            self.__class__.__name__, self.new, self._changed,
            self._mapping)

    @property
    def new(self):
        return self._identity is None

    @property
    def identity(self):
        return self._identity

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


class _SessionFactory:
    """Session factory.
    """

    def __init__(self, *, session_id_store, backend_store, loop=None):
        if loop is None:
            loop = asyncio.get_event_loop()
        self._loop = loop
        assert isinstance(session_id_store, SessionIdStore), session_id_store
        assert isinstance(backend_store, SessionBackendStore), backend_store
        self._sid_store = session_id_store
        self._backend = backend_store

    def __call__(self, request, fut):
        """Instantiate Session object.
        """
        return asyncio.Task(self._load(request, fut), loop=self._loop)

    @asyncio.coroutine
    def _load(self, request, fut):
        """Load or create new session.
        """
        try:
            session_id = self._sid_store.get_session_id(request)
            if session_id is None:
                sess = Session()
            else:
                data, ident = yield from self._backend.load_session_data(
                    session_id)
                sess = Session(data, identity=ident)
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
        session_id = yield from self._backend.save_session_data(session)
        self._sid_store.put_session_id(request, session_id)


def create_session_factory(session_id_store, backend_store, loop=None):
    """Creates new session factory.

    Create new session factory from two storage:
    session_id_store and backend_store.
    """
    return _SessionFactory(session_id_store=session_id_store,
                           backend_store=backend_store,
                           loop=loop)
