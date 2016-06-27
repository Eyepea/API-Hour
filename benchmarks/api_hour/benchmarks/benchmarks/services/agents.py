import asyncio


async def list(container):
    pg = await container.engines['pg']

    with (await pg.cursor()) as cur:
        await cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM %(schema)s.agentfeatures af LEFT JOIN %(schema)s.agent_login_status als ON (af.id = als.agent_id)" % {'schema': container.config['engines']['pg']['schema']})
        return (await cur.fetchall())