import unittest
import email
import aiohttp

from unittest import mock

from aiorest import Request


class CookiesTests(unittest.TestCase):
    _REQUEST = aiohttp.RawRequestMessage(
        'GET', '/some/path', '1.1', (), True, None)

    def test_no_request_cookies(self):
        req = Request('host', aiohttp.RawRequestMessage(
            'GET', '/some/path', '1.1', (), True, None),
            email.message.Message(), None, loop=None)

        self.assertEqual(req.cookies, {})

        cookies = req.cookies
        self.assertIs(cookies, req.cookies)

    def test_request_cookie(self):
        headers = email.message.Message()
        headers['COOKIE'] = 'cookie1=value1; cookie2=value2'
        req = Request('host', self._REQUEST, headers, None, loop=None)

        self.assertEqual(req.cookies, {
            'cookie1': 'value1',
            'cookie2': 'value2',
            })

    def test_request_cookie__set_item(self):
        headers = email.message.Message()
        headers['COOKIE'] = 'name=value';

        req = Request('host', self._REQUEST, headers, None, loop=None)
        self.assertEqual(req.cookies, {'name': 'value'})

        with self.assertRaises(TypeError):
            req.cookies['my'] = 'value'
