import asyncio
import aiopg
import psycopg2
import psycopg2.extras

from .. import services


def agents_with_psycopg2_sync(request):
    # Only for this benchmark, don't use that on production
    conn = psycopg2.connect(host='127.0.0.1',
                            port=5432,
                            dbname='picard',
                            user='asterisk',
                            password='proformatique',
                            cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM agentfeatures af LEFT JOIN agent_login_status als ON (af.id = als.agent_id)")
    agents = cur.fetchall()
    conn.close()
    return agents

@asyncio.coroutine
def agents_with_psycopg2_async(request):
    # Only for this benchmark, don't use that on production
    conn = yield from aiopg.connect(host='127.0.0.1',
                                    port=5432,
                                    dbname='picard',
                                    user='asterisk',
                                    password='proformatique',
                                    cursor_factory=psycopg2.extras.RealDictCursor)
    cur = yield from conn.cursor()
    yield from cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM agentfeatures af LEFT JOIN agent_login_status als ON (af.id = als.agent_id)")
    agents = yield from cur.fetchall()
    yield from conn.close()
    return agents

@asyncio.coroutine
def agents_with_psycopg2_async_pool(request):
    return (yield from services.agents.list(request.application.ah_container))