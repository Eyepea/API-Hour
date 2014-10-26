import unittest
import asyncio
from unittest import mock

from api_hour.session import Session
from api_hour.session.base import _SessionFactory, create_session_factory
from api_hour.session.interface import SessionIdStore, SessionBackendStore


class SessionFactoryTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)
        self.dummy_sid = mock.Mock(__class__=SessionIdStore)
        self.dummy_storage = mock.Mock(__class__=SessionBackendStore)

    def tearDown(self):
        self.loop.close()
        del self.dummy_sid
        del self.dummy_storage

    def test_global_event_loop(self):
        asyncio.set_event_loop(self.loop)

        factory = create_session_factory(self.dummy_sid, self.dummy_storage)
        self.assertIsInstance(factory, _SessionFactory)
        self.assertIs(factory._loop, self.loop)

    def test_asserts(self):
        with self.assertRaises(AssertionError):
            create_session_factory(None, self.dummy_storage, loop=self.loop)
        with self.assertRaises(AssertionError):
            create_session_factory(self.dummy_sid, None, loop=self.loop)

    def test_create_new_session(self):
        factory = create_session_factory(self.dummy_sid, self.dummy_storage,
                                         loop=self.loop)

        @asyncio.coroutine
        def load(session_id):
            return (None, None)

        self.dummy_storage.load_session_data.side_effect = load

        @asyncio.coroutine
        def go():
            waiter = asyncio.Future(loop=self.loop)
            req = mock.Mock()

            factory(req, waiter)

            sess = yield from asyncio.wait_for(waiter, timeout=1,
                                               loop=self.loop)

            self.assertIsInstance(sess, Session)
            self.assertTrue(sess.new)
            self.assertIsNone(sess.identity)
            req.add_response_callback.assert_called_once_with(
                factory._save, session=sess)

        self.loop.run_until_complete(go())

        self.dummy_storage.save_session_data.assert_call_count(0)

    def test_load_existing_session(self):
        factory = create_session_factory(self.dummy_sid, self.dummy_storage,
                                         loop=self.loop)
        request = mock.Mock()

        self.dummy_sid.get_session_id.return_value = 123

        @asyncio.coroutine
        def load(session_id):
            self.assertEqual(session_id, 123)
            return ({'foo': 'bar'}, 321)

        self.dummy_storage.load_session_data.side_effect = load

        @asyncio.coroutine
        def go():
            waiter = asyncio.Future(loop=self.loop)
            factory(request, waiter)
            sess = yield from asyncio.wait_for(waiter, timeout=1,
                                               loop=self.loop)

            self.assertEqual(dict(sess), {'foo': 'bar'})
            self.dummy_sid.get_session_id.assert_called_once_with(request)
            request.add_response_callback.assert_called_once_with(
                factory._save, session=sess)

        self.loop.run_until_complete(go())
        self.dummy_storage.save_session_data.assert_call_count(0)

    def test_load_and_save(self):
        factory = create_session_factory(self.dummy_sid, self.dummy_storage,
                                         loop=self.loop)

        @asyncio.coroutine
        def load(session_id):
            return (None, None)

        @asyncio.coroutine
        def save(session):
            return

        self.dummy_storage.load_session_data.side_effect = load
        self.dummy_storage.save_session_data.side_effect = save

        @asyncio.coroutine
        def go():
            waiter = asyncio.Future(loop=self.loop)
            req = mock.Mock()

            factory(req, waiter)

            sess = yield from asyncio.wait_for(waiter, timeout=1,
                                               loop=self.loop)

            self.assertIsInstance(sess, Session)
            self.assertTrue(sess.new)
            self.assertIsNone(sess.identity)
            req.add_response_callback.assert_called_once_with(
                factory._save, session=sess)

            yield from factory._save(req, session=sess)
            self.dummy_storage.save_session_data.assert_call_count(0)

            sess['foo'] = 'bar'
            yield from factory._save(req, session=sess)
            self.dummy_storage.save_session_data.assert_call_once_with(sess)

        self.loop.run_until_complete(go())

        self.dummy_storage.save_session_data.assert_call_count(0)
