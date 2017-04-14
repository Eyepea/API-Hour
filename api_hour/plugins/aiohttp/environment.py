import logging

try:
    import ujson as json
except ImportError:
    import json

from . import JSON

LOG = logging.getLogger(__name__)


async def env_middleware_factory(app, handler):
    async def env_middleware(request):

        LOG.debug('incoming request %s from: %s', request.method, request.path)
        request['env'] = {
            'container': request.app['ah_container'],
            'id': request.headers.get('Request_ID', None)
        }

        try:
            name = request.match_info.route.resource.name
            config = request['env']['container'].env_config.get(name, [])
        except AttributeError:
            LOG.debug('Can not retrieve resource name for %(http_path)s', {'http_path': request.path})
            return await handler(request)

        LOG.debug('Resource name: %s, config: %s', name, config)

        if 'pg' in config and 'pg' in request['env']['container'].engines:
            LOG.debug('Creating pg cursor')
            request['env']['pg'] = dict()
            request['env']['pg']['engine'] = await request['env']['container'].engines['pg']
            request['env']['pg']['cursor_context_manager'] = await request['env']['pg']['engine'].cursor()
            request['env']['pg']['cursor'] = request['env']['pg']['cursor_context_manager'].__enter__()
            await request['env']['pg']['cursor'].execute('BEGIN')

        if 'mysql' in config and 'mysql' in request['env']['container'].engines:
            LOG.debug('Creating mysql cursor')
            request['env']['mysql'] = dict()
            request['env']['mysql']['engine'] = await request['env']['container'].engines['mysql']
            request['env']['mysql']['connection'] = await request['env']['mysql']['engine'].acquire()
            request['env']['mysql']['cursor'] = await request['env']['mysql']['connection'].cursor()
            await request['env']['mysql']['connection'].begin()

        if 'redis' in config and 'redis' in request['env']['container'].engines:
            LOG.debug('Creating redis connection')
            request['env']['redis'] = dict()
            request['env']['redis']['engine'] = await request['env']['container'].engines['redis']
            request['env']['redis']['connection'] = await request['env']['redis']['engine'].acquire()

        if 'json' in config:
            LOG.debug('Parsing json')
            try:
                request['env']['json'] = await request.json(loads=json.loads)
            except ValueError:
                raise JSON(status=400, data='''The payload must be of json format''')
            LOG.debug('Json parsed')

        request['env']['name'] = name
        request['env']['config'] = config

        try:
            LOG.debug('Handling request')
            response = await handler(request)
        except Exception as exception:
            if 'pg' in config and 'pg' in request['env'] and not request['env']['pg']['cursor'].closed:
                LOG.debug('Rolling back postgres transaction')
                await request['env']['pg']['cursor'].execute('ROLLBACK')
                request['env']['pg']['cursor_context_manager'].__exit__()

            if 'mysql' in config and 'mysql' in request['env'] and not request['env']['mysql']['cursor'].closed:
                LOG.debug('Rolling back mysql transaction')
                await request['env']['mysql']['connection'].rollback()
                await request['env']['mysql']['cursor'].close()
                request['env']['mysql']['engine'].release(request['env']['mysql']['connection'])
            raise exception
        else:
            if 'pg' in config and 'pg' in request['env'] and not request['env']['pg']['cursor'].closed:
                LOG.debug('Committing postgres transaction')
                await request['env']['pg']['cursor'].execute('COMMIT')
                request['env']['pg']['cursor_context_manager'].__exit__()

            if 'mysql' in config and 'mysql' in request['env'] and not request['env']['mysql']['cursor'].closed:
                LOG.debug('Committing mysql transaction')
                await request['env']['mysql']['connection'].commit()
                await request['env']['mysql']['cursor'].close()
                request['env']['mysql']['engine'].release(request['env']['mysql']['connection'])
        finally:
            if 'redis' in config and 'redis' in request['env'] and not request['env']['redis']['connection'].closed:
                LOG.debug('Closing redis connection')
                request['env']['redis']['connection'].close()
                await request['env']['redis']['connection'].wait_closed()

        return response

    return env_middleware
