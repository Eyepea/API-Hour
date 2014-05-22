import unittest
import email
import aiohttp

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
        resp = Response(loop=self.loop)

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

    def test_response_cookie__issue_del_cookie(self):
        resp = Response(loop=self.loop)
        self.assertEqual(resp.cookies, {})
        self.assertEqual(str(resp.cookies), '')

        resp.del_cookie('name')
        self.assertEqual(str(resp.cookies), 'Set-Cookie: name=; Max-Age=0')
