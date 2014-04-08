import unittest
import asyncio
import pickle

from unittest import mock
from asyncio_redis import Connection
from asyncio_redis.encoders import BytesEncoder

from aiorest.redis_session import RedisSessionFactory


class RedisSessionTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        # FIXME: asyncio_redis doesn't like to pass loop explicitly
        asyncio.set_event_loop(self.loop)

        self.redis = self.loop.run_until_complete(
            Connection.create(db=0, encoder=BytesEncoder(),
                              loop=self.loop))

    def tearDown(self):
        self.loop.run_until_complete(self.redis.flushdb())
        self.loop.close()

    def test_load_empty(self):
        factory = RedisSessionFactory(self.redis, 'secret', 'test',
                                      loop=self.loop)

        req = mock.Mock()
        req.cookies.get.return_value = factory._encode_cookie('123')

        @asyncio.coroutine
        def run():
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            sess = yield from fut
            self.assertEqual(sess, {})
            self.assertTrue(sess.new)

        self.loop.run_until_complete(run())

    def test_load_existent(self):
        factory = RedisSessionFactory(self.redis, 'secret', 'test',
                                      loop=self.loop)
        req = mock.Mock()
        req.cookies.get.return_value = factory._encode_cookie('123')

        key = b'session:123'
        data = pickle.dumps({'foo': 'bar'}, protocol=pickle.HIGHEST_PROTOCOL)
        ok = self.loop.run_until_complete(self.redis.set(key, data))
        self.assertTrue(ok)

        @asyncio.coroutine
        def run():
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            sess = yield from fut
            self.assertFalse(sess.new)
            self.assertEqual(sess, {'foo': 'bar'})
        self.loop.run_until_complete(run())
