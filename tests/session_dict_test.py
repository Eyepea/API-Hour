import unittest

from aiorest.session import Session


class SessionTests(unittest.TestCase):

    def test_create(self):
        s = Session()
        self.assertEqual(s, {})
        self.assertTrue(s.new)
        self.assertIsNone(s.identity)
        self.assertFalse(s._changed)

        s = Session({'some': 'data'})
        self.assertEqual(s, {'some': 'data'})
        self.assertTrue(s.new)
        self.assertIsNone(s.identity)
        self.assertFalse(s._changed)

        s = Session(identity=1)
        self.assertEqual(s, {})
        self.assertFalse(s.new)
        self.assertEqual(s.identity, 1)
        self.assertFalse(s._changed)

    def test_create_error(self):
        with self.assertRaises(ValueError):
            Session('abc')
        with self.assertRaises(TypeError):
            Session([1, 2, 3])
        with self.assertRaises(TypeError):
            Session(int)

    def test__repr__(self):
        s = Session()
        self.assertEqual(str(s), '<Session [new:True, changed:False] {}>')
        s['foo'] = 'bar'
        self.assertEqual(str(s),
            "<Session [new:True, changed:True] {'foo': 'bar'}>")
        s = Session({'key': 123}, identity=1)
        self.assertEqual(str(s),
            "<Session [new:False, changed:False] {'key': 123}>")
        s.invalidate()
        self.assertEqual(str(s),
            "<Session [new:False, changed:True] {}>")

    def test_invalidate(self):
        s = Session({'foo': 'bar'})
        self.assertEqual(s, {'foo': 'bar'})
        self.assertTrue(s.new)
        self.assertIsNone(s.identity)
        self.assertFalse(s._changed)

        s.invalidate()
        self.assertEqual(s, {})
        self.assertTrue(s.new)
        self.assertIsNone(s.identity)
        self.assertTrue(s._changed)

        s = Session({'foo': 'bar'}, identity=1)
        self.assertEqual(s, {'foo': 'bar'})
        self.assertFalse(s.new)
        self.assertEqual(s.identity, 1)
        self.assertFalse(s._changed)

        s.invalidate()
        self.assertEqual(s, {})
        self.assertFalse(s.new)
        self.assertEqual(s.identity, 1)
        self.assertTrue(s._changed)

    def test_operations(self):
        s = Session()
        self.assertEqual(s, {})
        self.assertEqual(len(s), 0)
        self.assertEqual(list(s), [])
        self.assertNotIn('foo', s)
        self.assertNotIn('key', s)

        s = Session({'foo': 'bar'})
        self.assertEqual(len(s), 1)
        self.assertEqual(s, {'foo': 'bar'})
        self.assertEqual(list(s), ['foo'])
        self.assertIn('foo', s)
        self.assertNotIn('key', s)

        s['key'] = 'value'
        self.assertEqual(len(s), 2)
        self.assertEqual(s, {'foo': 'bar', 'key': 'value'})
        self.assertEqual(sorted(s), ['foo', 'key'])
        self.assertIn('foo', s)
        self.assertIn('key', s)

        del s['key']
        self.assertEqual(len(s), 1)
        self.assertEqual(s, {'foo': 'bar'})
        self.assertEqual(list(s), ['foo'])
        self.assertIn('foo', s)
        self.assertNotIn('key', s)

        s.pop('foo')
        self.assertEqual(len(s), 0)
        self.assertEqual(s, {})
        self.assertEqual(list(s), [])
        self.assertNotIn('foo', s)
        self.assertNotIn('key', s)
