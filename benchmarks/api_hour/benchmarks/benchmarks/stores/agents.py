import asyncio


@asyncio.coroutine
def list(application):
    with (yield from application.engines['pg'].cursor()) as cur:
        yield from cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM agentfeatures af LEFT JOIN agent_login_status als ON (af.id = als.agent_id)")
        agents = yield from cur.fetchall()
    return agents