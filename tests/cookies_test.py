import unittest
import email
import aiohttp
import asyncio

from unittest import mock

from aiorest import Request, Response


class CookiesTests(unittest.TestCase):
    _REQUEST = aiohttp.RawRequestMessage(
        'GET', '/some/path', '1.1', (), True, None)

    def setUp(self):
        self.loop = mock.Mock()

    def test_no_request_cookies(self):
        req = Request('host', aiohttp.RawRequestMessage(
            'GET', '/some/path', '1.1', (), True, None),
            email.message.Message(), None, loop=self.loop)

        self.assertEqual(req.cookies, {})

        cookies = req.cookies
        self.assertIs(cookies, req.cookies)

    def test_request_cookie(self):
        headers = email.message.Message()
        headers['COOKIE'] = 'cookie1=value1; cookie2=value2'
        req = Request('host', self._REQUEST, headers, None, loop=self.loop)

        self.assertEqual(req.cookies, {
            'cookie1': 'value1',
            'cookie2': 'value2',
            })

    def test_request_cookie__set_item(self):
        headers = email.message.Message()
        headers['COOKIE'] = 'name=value'

        req = Request('host', self._REQUEST, headers, None, loop=self.loop)
        self.assertEqual(req.cookies, {'name': 'value'})

        with self.assertRaises(TypeError):
            req.cookies['my'] = 'value'

    def test_response_cookies(self):
        resp = Response()

        self.assertEqual(resp.cookies, {})
        self.assertEqual(str(resp.cookies), '')

        resp.set_cookie('name', 'value')
        self.assertEqual(str(resp.cookies), 'Set-Cookie: name=value')
        resp.set_cookie('name', 'other_value')
        self.assertEqual(str(resp.cookies), 'Set-Cookie: name=other_value')

        resp.cookies['name'] = 'another_other_value'
        resp.cookies['name']['max-age'] = 10
        self.assertEqual(str(resp.cookies),
                         'Set-Cookie: name=another_other_value; Max-Age=10')

        resp.del_cookie('name')
        self.assertEqual(str(resp.cookies), 'Set-Cookie: name=; Max-Age=0')

        resp.set_cookie('name', 'value', domain='local.host')
        self.assertEqual(str(resp.cookies),
                         'Set-Cookie: name=value; Domain=local.host')

    def test_response_cookie_path(self):
        resp = Response()
        self.assertEqual(resp.cookies, {})

        resp.set_cookie('name', 'value', path='/some/path')
        self.assertEqual(str(resp.cookies),
                         'Set-Cookie: name=value; Path=/some/path')
        resp.set_cookie('name', 'value', expires='123')
        self.assertEqual(str(resp.cookies),
                         'Set-Cookie: name=value; expires=123;'
                         ' Path=/some/path')
        resp.set_cookie('name', 'value', domain='example.com',
                        path='/home', expires='123', max_age='10',
                        secure=True, httponly=True, version='2.0')
        self.assertEqual(str(resp.cookies),
                         'Set-Cookie: name=value; '
                         'Domain=example.com; '
                         'expires=123; '
                         'httponly; '
                         'Max-Age=10; '
                         'Path=/home; '
                         'secure; '
                         'Version=2.0')

    def test_response_cookie__issue_del_cookie(self):
        resp = Response()
        self.assertEqual(resp.cookies, {})
        self.assertEqual(str(resp.cookies), '')

        resp.del_cookie('name')
        self.assertEqual(str(resp.cookies), 'Set-Cookie: name=; Max-Age=0')

    def test_global_event_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        req = Request('host', self._REQUEST, email.message.Message(), None)
        self.assertIs(req._loop, loop)

        loop.close()
