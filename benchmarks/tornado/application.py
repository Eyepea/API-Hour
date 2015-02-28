#!/usr/bin/env python3
from tornado import gen
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer
from tornado.options import parse_command_line
from tornado.web import RequestHandler, Application, asynchronous

import psycopg2
import momoko


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

class Index(RequestHandler):
    def get(self):
        self.write({'hello': 'world'})
        self.finish()


class AgentsPool(BaseHandler):
    @gen.coroutine
    def get(self):
        query = """
                SELECT
                    af.number AS number,
                    als.extension AS extension,
                    als.context AS context,
                    als.state_interface AS state_interface,
                    'offline' AS status,
                    '-1' AS extension_status,
                    '0' AS paused
                FROM
                    public.agentfeatures af
                    LEFT JOIN public.agent_login_status als ON (af.id = als.agent_id)
                """
        try:
            cursor = yield momoko.Op(self.db.execute, query)
        except (psycopg2.Warning, psycopg2.Error) as error:
            self.write(str(error))
        else:
            self.write("Results: %r" % (cursor.fetchall(),))

        self.finish()

if __name__ == '__main__':
    parse_command_line()
    application = Application([
        (r'/agents_with_pool', AgentsPool),
        (r'/index', Index),
    ], debug=False)

    application.db = momoko.Pool(
        dsn='dbname=benchmarks user=asterisk password=asterisk host=127.0.0.1 port=5432',
        size=1
    )

    http_server = HTTPServer(application)
    http_server.listen(8000, 'localhost')
    IOLoop.instance().start()