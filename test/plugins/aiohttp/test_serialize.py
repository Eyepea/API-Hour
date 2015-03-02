from api_hour.plugins.aiohttp import JSON
from api_hour.plugins.aiohttp import HTML


def test_json_body():
    x = JSON({'foo': 'bar'})
    assert x._body == b'{"foo":"bar"}'


def test_json_content_type():
    x = JSON({'foo': 'bar'})
    assert x._content_type == 'application/json'


def test_html_body():
    x = HTML('<html>test</html>')
    assert x._body == b'<html>test</html>'


def test_html_content_type():
    x = HTML('<html>test</html>')
    assert x._content_type == 'text/html'
