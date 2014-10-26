#!/usr/bin/env python3

import json

from flask import Flask
import psycopg2, psycopg2.extras

app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return json.dumps({'hello': 'world'})

@app.route('/agents')
def agents():
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
    return json.dumps(agents)

if __name__ == '__main__':
    app.run()