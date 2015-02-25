#!/usr/bin/env python3

import json

from flask import Flask
import psycopg2, psycopg2.extras, psycopg2.pool

app = Flask(__name__)

@app.route('/index')
def index():
    return json.dumps({'hello': 'world'})

p = psycopg2.pool.ThreadedConnectionPool(30, 30, host='127.0.0.1',
                                            port=5432,
                                            dbname='benchmarks',
                                            user='asterisk',
                                            password='asterisk',
                                            cursor_factory=psycopg2.extras.RealDictCursor)


@app.route('/agents_with_pool')
def agents_with_pool():
    global p
    conn = p.getconn()
    cur = conn.cursor()
    cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM public.agentfeatures af LEFT JOIN public.agent_login_status als ON (af.id = als.agent_id)")
    agents = cur.fetchall()
    conn.close()
    return json.dumps(agents)

@app.route('/agents')
def agents():
    conn = psycopg2.connect(host='127.0.0.1',
                            port=5432,
                            dbname='benchmarks',
                            user='asterisk',
                            password='asterisk',
                            cursor_factory=psycopg2.extras.RealDictCursor)
    cur = conn.cursor()
    cur.execute("SELECT af.number AS number, als.extension AS extension, als.context AS context, als.state_interface AS state_interface, 'offline' AS status, '-1' AS extension_status, '0' AS paused FROM public.agentfeatures af LEFT JOIN public.agent_login_status als ON (af.id = als.agent_id)")
    agents = cur.fetchall()
    conn.close()
    return json.dumps(agents)

if __name__ == '__main__':
    app.run(debug=True)