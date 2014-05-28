import unittest
import asyncio
import json
import hmac as _hmac

from unittest import mock
from aiorest.session import (
    Session,
    # SecureCookie,
    # BaseSessionFactory,
    # CookieSessionFactory,
    )


@unittest.skip("sessions was refactored, this test makes too little sense now")
class BaseSessionFactoryTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

    def tearDown(self):
        self.loop.close()

    def test_simple(self):
        req = mock.Mock()
        req.cookies.get.return_value = ''
        fut = asyncio.Future(loop=self.loop)

        @asyncio.coroutine
        def run():
            factory = BaseSessionFactory('secret', 'test_cookie',
                                         loop=self.loop)
            factory(req, fut)

            session = yield from fut
            self.assertEqual(session, {})
            self.assertTrue(session.new)
            self.assertFalse(session._changed)

            req.cookies.get.assert_called_with('test_cookie')
            req.add_response_callback.assert_called_once_with(factory._save,
                                                              session=session)

            session.changed()
            self.assertTrue(session._changed)

            with self.assertRaises(NotImplementedError):
                yield from factory._save(req, session=session)

        self.loop.run_until_complete(run())

    @mock.patch('aiorest.session.cookie_session.hmac')
    def _test_load_exception(self, hmac_mock):
        req = mock.Mock()
        req.cookies.get.return_value = '[bad json]|1|sign'
        hmac_mock.compare_digest.return_value = True

        @asyncio.coroutine
        def run():
            factory = BaseSessionFactory('secret', 'test_cookie',
                                         loop=self.loop)
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            with self.assertRaises(NotImplementedError):
                yield from fut

            factory = CookieSessionFactory(json.loads, json.dumps,
                                           secret_key='secret',
                                           cookie_name='test_cookie',
                                           loop=self.loop)
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            sess = yield from fut
            self.assertTrue(sess.new)
            self.assertEqual(sess, {})

        self.loop.run_until_complete(run())

    @mock.patch('aiorest.session.cookie_session.time')
    @mock.patch('aiorest.session.cookie_session.hmac')
    def _test__encode_cookie(self, hmac_mock, time_mock):
        time_mock.time.return_value = 1
        hmac_mock.new.return_value = sign_mock = mock.Mock()
        sign_mock.hexdigest.return_value = 'code'

        factory = BaseSessionFactory('secret', 'test', loop=self.loop)

        ret = factory._encode_cookie('123')
        self.assertEqual(ret, '123|1|code')

        sign_mock.update.assert_called_with(b'test|123|1')

    @mock.patch('aiorest.session.cookie_session.hmac')
    def _test__decode_cookie(self, hmac_mock):
        hmac_mock.new.return_value = sign_mock = mock.Mock()
        sign_mock.hexdigest.return_value = 'code'

        factory = BaseSessionFactory('secret', 'test', loop=self.loop)

        ret = factory._decode_cookie('')
        self.assertIsNone(ret)
        self.assertEqual(hmac_mock.new.call_count, 0)

        ret = factory._decode_cookie('bad value')
        self.assertIsNone(ret)
        self.assertEqual(hmac_mock.new.call_count, 0)

        ret = factory._decode_cookie('bad|value')
        self.assertIsNone(ret)
        self.assertEqual(hmac_mock.new.call_count, 0)

        ret = factory._decode_cookie('still|this is a|bad|value')
        self.assertIsNone(ret)
        self.assertEqual(hmac_mock.new.call_count, 0)

        ret = factory._decode_cookie('foo|1|code')
        self.assertEqual(ret, 'foo')
        hmac_mock.new.assert_called_with(b'secret', digestmod=mock.ANY)
        hmac_mock.compare_digest.assert_called_with('code', 'code')
        sign_mock.update.assert_called_with(b'test|foo|1')

    @mock.patch('aiorest.session.cookie_session.hmac')
    def _test__decode_cookie__signature_mismatch(self, hmac_mock):
        hmac_mock.new.return_value = sign_mock = mock.Mock()

        def compare(a, b):
            ret = _hmac.compare_digest(a, b)
            self.assertFalse(ret)
            return ret

        hmac_mock.compare_digest.side_effect = compare
        sign_mock.hexdigest.return_value = 'code'

        factory = BaseSessionFactory('secret', 'test', loop=self.loop)
        ret = factory._decode_cookie('foo|1|bad_sign')
        self.assertIsNone(ret)
        hmac_mock.compare_digest.assert_called_with('code', 'bad_sign')

    @mock.patch('aiorest.session.cookie_session.time')
    @mock.patch('aiorest.session.cookie_session.hmac')
    def _test__decode_cookie__expire(self, hmac_mock, time_mock):
        time_mock.time.return_value = 100
        hmac_mock.new.return_value = sign_mock = mock.Mock()
        sign_mock.hexdigest.return_value = 'code'

        factory = BaseSessionFactory('secret', 'test', session_max_age=10,
                                     loop=self.loop)
        ret = factory._decode_cookie('foo|1|bad_sign')
        self.assertIsNone(ret)

        time_mock.time.return_value = 9
        ret = factory._decode_cookie('foo|1|code')
        self.assertEqual(ret, 'foo')

    def test_cookie_session_load(self):
        loads_mock = mock.Mock()
        loads_mock.side_effect = lambda obj: obj
        dumps_mock = mock.Mock()
        factory = CookieSessionFactory(loads_mock, dumps_mock,
                                       secret_key='secret',
                                       cookie_name='test',
                                       loop=self.loop)

        @asyncio.coroutine
        def run():
            data, id = yield from factory.load_session_data('some value')
            self.assertEqual(data, 'some value')
            self.assertEqual(id, '')

        self.loop.run_until_complete(run())

        loads_mock.assert_called_with('some value')
        self.assertEqual(dumps_mock.call_count, 0)

    def test_cookie_session_load__error(self):
        dumps_mock = mock.Mock()
        factory = CookieSessionFactory(json.loads, dumps_mock,
                                       secret_key='secret',
                                       cookie_name='test',
                                       loop=self.loop)

        @asyncio.coroutine
        def run():
            data, id = yield from factory.load_session_data(None)
            self.assertIsNone(data)
            self.assertIsNone(id)
            data, id = yield from factory.load_session_data('[not json value]')
            self.assertIsNone(data)
            self.assertIsNone(id)
        self.loop.run_until_complete(run())
        self.assertEqual(dumps_mock.call_count, 0)

    def test_cookie_session_save(self):
        loads_mock = mock.Mock()
        factory = CookieSessionFactory(loads_mock, json.dumps,
                                       secret_key='secret',
                                       cookie_name='test',
                                       loop=self.loop)

        @asyncio.coroutine
        def run():
            ret = yield from factory.save_session_data({'foo': 'bar'})
            self.assertEqual(ret, '{"foo": "bar"}')
            sess = Session()
            sess['foo'] = 'bar'
            ret = yield from factory.save_session_data(sess)
            self.assertEqual(ret, '{"foo": "bar"}')

            ret = yield from factory.save_session_data(Session())
            self.assertIsNone(ret)
            ret = yield from factory.save_session_data({})
            self.assertIsNone(ret)

        self.loop.run_until_complete(run())
