import asyncio
import aiorest


@asyncio.coroutine
@aiorest.serialize.to('html')
def index(request):
    '''Seiralize coroutine with decorator'''
    yield from asyncio.sleep(1)
    return '''
        <!DOCTYPE html>
        <link rel="icon" type="image/x-icon" href="/favicon.ico">
        <h1>Hello</h1>
    '''


def favicon(request):
    '''Return serialized data'''
    with open('favicon.ico', 'rb') as f:
        content = f.read()
        return aiorest.serialize.Asset(content, content_type='image/x-icon')


loop = asyncio.get_event_loop()
server = aiorest.RESTServer(hostname='127.0.0.1', loop=loop)

# configure routes
server.add_url('GET', '/', index)
server.add_url('GET', '/favicon.ico', favicon)

# create server
srv = loop.run_until_complete(loop.create_server(
    server.make_handler, '127.0.0.1', 8000))
loop.run_forever()
