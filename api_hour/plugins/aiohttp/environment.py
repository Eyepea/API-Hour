import logging

try:
    import ujson as json
except ImportError:
    import json

from . import JSON

LOG = logging.getLogger(__name__)


async def env_middleware_factory(app, handler):
    async def env_middleware(request):
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

        if 'pg' in config and 'pg' in request['env']['container'].engines:
            request['env']['pg'] = dict()
            request['env']['pg']['engine'] = await request['env']['container'].engines['pg']
            request['env']['pg']['cursor_context_manager'] = await request['env']['pg']['engine'].cursor()
            request['env']['pg']['cursor'] = request['env']['pg']['cursor_context_manager'].__enter__()
            await request['env']['pg']['cursor'].execute('BEGIN')

        if 'mysql' in config and 'mysql' in request['env']['container'].engines:
            request['env']['mysql'] = dict()
            request['env']['mysql']['engine'] = await request['env']['container'].engines['mysql']
            request['env']['mysql']['connection'] = await request['env']['mysql']['engine'].acquire()
            request['env']['mysql']['cursor'] = await request['env']['mysql']['connection'].cursor()
            await request['env']['mysql']['connection'].begin()

        if 'redis' in config and 'redis' in request['env']['container'].engines:
            request['env']['redis'] = dict()
            request['env']['redis']['engine'] = await request['env']['container'].engines['redis']
            request['env']['redis']['connection'] = await request['env']['redis']['engine'].acquire()

        if 'json' in config:
            try:
                request['env']['json'] = await request.json(loads=json.loads)
            except ValueError:
                raise JSON(status=400, data='''The payload must be of json format''')

        request['env']['name'] = name
        request['env']['config'] = config

        try:
            response = await handler(request)
        except Exception as exception:
            if 'pg' in config and 'pg' in request['env'] and not request['env']['pg']['cursor'].closed:
                LOG.debug('Rolling back postgres transaction')
                await request['env']['pg']['cursor'].execute('ROLLBACK')
                request['env']['pg']['cursor_context_manager'].__exit__()

            if 'mysql' in config and 'mysql' in request['env'] and not request['env']['mysql']['cursor'].closed:
                LOG.debug('Rolling back mysql transaction')
                await request['env']['mysql']['connection'].rollback()
                request['env']['mysql']['connection'].close()

            raise exception
        else:
            if 'pg' in config and 'pg' in request['env'] and not request['env']['pg']['cursor'].closed:
                LOG.debug('Committing postgres transaction')
                await request['env']['pg']['cursor'].execute('COMMIT')
                request['env']['pg']['cursor_context_manager'].__exit__()

            if 'mysql' in config and 'mysql' in request['env'] and not request['env']['mysql']['cursor'].closed:
                LOG.debug('Committing mysql transaction')
                await request['env']['mysql']['connection'].commit()
                request['env']['mysql']['connection'].close()
        finally:
            if 'redis' in config and 'redis' in request['env'] and not request['env']['redis']['connection'].closed:
                LOG.debug('Closing redis connection')
                request['env']['redis']['connection'].close()
                await request['env']['redis']['connection'].wait_closed()

        return response

    return env_middleware
