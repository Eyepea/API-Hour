import abc
import asyncio


__all__ = ['SessionIdStore', 'SessionBackendStore']


class SessionIdStore(metaclass=abc.ABCMeta):
    """Abstract iterface.
    """

    @abc.abstractmethod
    def get_session_id(self, request):
        """Gets session ID from request.

        This method must return session id or None.
        If None is returned new empty session is created.

        This method MUST NOT be a coroutine.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def put_session_id(self, request, session_id):
        """Puts session id in response (through given request argument).

        This method is called when session is saved.
        session_id argument may be None meaning session has been deleted.
        Implementations of this method must handle this case.

        This method MUST NOT be a coroutine.
        """
        raise NotImplementedError


class SessionBackendStore(metaclass=abc.ABCMeta):
    """Abstract backend session storage interface.
    """

    @abc.abstractmethod
    @asyncio.coroutine
    def load_session_data(self, session_id):
        """Loads session data based on value of session_id.

        Must returns tuple: session data dict and session id.
        If no valid data can be found implementation must
        return (None, None) tuple.

        This method MUST be a coroutine.
        """
        raise NotImplementedError

    @abc.abstractmethod
    @asyncio.coroutine
    def save_session_data(self, session):
        """Stores session data and returns session_id.

        This method MUST be a coroutine.
        """
        raise NotImplementedError
