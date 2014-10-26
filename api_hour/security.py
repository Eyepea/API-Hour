import abc
import asyncio

# see http://plope.com/pyramid_auth_design_api_postmortem


class AbstractIdentityPolicy(metaclass=abc.ABCMeta):

    @asyncio.coroutine
    @abc.abstractmethod
    def identify(self, request):
        """ Return the claimed identity of the user associated request or
        ``None`` if no identity can be found associated with the request."""
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def remember(self, request, identity, **kw):
        """ Modify request.response which
        can be used to remember ``identity`` for a subsequent request.
        An individual identity policy and its consumers can decide on
        the composition and meaning of **kw."""
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def forget(self, request):
        """ Modify request.response which
        can be used to 'forget' the current identity
        on subsequent requests."""
        pass


class AbstractAuthorizationPolicy(metaclass=abc.ABCMeta):

    @asyncio.coroutine
    @abc.abstractmethod
    def permits(self, user_id, permission, context=None):
        """ Return True if the user_id is allowed the permission in the
        current context, else return False"""
        pass

    @asyncio.coroutine
    @abc.abstractmethod
    def authorized_user_id(self, identity):
        """ Return the user_id of the user identified by the identity
        or 'None' if no user exists related to the identity """
        pass


class CookieIdentityPolicy(AbstractIdentityPolicy):

    @asyncio.coroutine
    def identify(self, request):
        return request.cookies.get('user_id', None)

    @asyncio.coroutine
    def remember(self, request, identity, **kw):
        request.response.set_cookie('user_id', identity)

    @asyncio.coroutine
    def forget(self, request):
        request.response.del_cookie('user_id')
