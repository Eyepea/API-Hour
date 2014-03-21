import unittest


from aiorest.router import Router, rest


class RouterTests(unittest.TestCase):

    def setUp(self):
        pass

    def test_add_handler(self):

        class TestHandler:

            @rest('/prefix/get', 'post')
            def get(self):
                return {'a': 1}

        router = Router()
        h = TestHandler()
        router.add_handler(h)

        self.assertIn(('/prefix/get', 'POST'), router._table)
        self.assertEqual(h.get, router._table[('/prefix/get', 'POST')])
