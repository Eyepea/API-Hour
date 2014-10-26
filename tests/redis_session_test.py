import unittest
import asyncio
import pickle
import aioredis
from unittest import mock

from api_hour.session import RedisSessionFactory


class RedisSessionTests(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(None)

        self.redis_pool = self.loop.run_until_complete(
            aioredis.create_pool(('localhost', 6379), db=0, loop=self.loop))

    @asyncio.coroutine
    def _flush(self):
        with (yield from self.redis_pool) as redis:
            yield from redis.flushdb()

    def tearDown(self):
        self.loop.run_until_complete(self._flush())
        self.loop.close()

    def test_load_empty(self):
        factory = RedisSessionFactory(self.redis_pool, 'secret', 'test',
                                      loop=self.loop)

        sid_store = factory._sid_store
        req = mock.Mock()
        req.cookies.get.return_value = sid_store._encode_cookie('123')

        @asyncio.coroutine
        def run():
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            sess = yield from fut
            self.assertEqual(sess, {})
            self.assertTrue(sess.new)

        self.loop.run_until_complete(run())

    def test_load_existent(self):
        factory = RedisSessionFactory(self.redis_pool, 'secret', 'test',
                                      loop=self.loop)
        sid_store = factory._sid_store
        req = mock.Mock()
        req.cookies.get.return_value = sid_store._encode_cookie('123')

        key = b'session:123'
        data = pickle.dumps({'foo': 'bar'}, protocol=pickle.HIGHEST_PROTOCOL)

        @asyncio.coroutine
        def run():
            with (yield from self.redis_pool) as redis:
                ok = yield from redis.set(key, data)
                self.assertTrue(ok)
            fut = asyncio.Future(loop=self.loop)
            factory(req, fut)
            sess = yield from fut
            self.assertFalse(sess.new)
            self.assertEqual(sess, {'foo': 'bar'})
        self.loop.run_until_complete(run())
