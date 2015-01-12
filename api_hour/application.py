# This file is part of API-Hour, forked from gunicorn/app/wsgiapp.py released under the MIT license.
import logging
import os
import sys

from gunicorn.app.base import Application as GunicornApp
from gunicorn import util
from gunicorn.config import Config

from .config import get_config


class Application(GunicornApp):
    def init(self, parser, opts, args):
        if len(args) < 1:
            parser.error("No application module specified.")

        self.cfg.set("default_proc_name", args[0])
        self.app_uri = args[0]

        logging.captureWarnings(True)
        if opts.auto_config:
            # Default config_dir
            config_dir = os.path.join(self.cfg.chdir,
                                      'etc',
                                      self.app_uri.split(":", 1)[0])
            if os.path.exists(config_dir):
                self.cfg.set('config_dir', config_dir)  # Define dev etc folder as default config directory

            # generate config_dir directly: egg or chicken problem
            if opts.config_dir:
                self.cfg.set('config_dir', opts.config_dir)

            if not opts.config:
                opts.config = os.path.join(self.cfg.config_dir, 'api_hour/gunicorn_conf.py')

            if not self.cfg.logconfig:
                self.cfg.set('logconfig', os.path.join(self.cfg.config_dir, 'api_hour/logging.ini'))
        else:
            # To avoid with Gunicorn 19 that the console it's empty when you test
            if not opts.errorlog:
                opts.errorlog = '-'
            if not opts.accesslog:
                opts.accesslog = '-'

    def load_default_config(self):
        # init configuration
        self.cfg = Config(self.usage, prog=self.prog)
        self.cfg.set('worker_class', 'api_hour.Worker')  # Define api_hour.Worker as default

    def load_config(self):
        # parse console args
        super().load_config()
        if self.cfg.config_dir:
            self.config = get_config({'config_dir': self.cfg.config_dir})
        else:
            self.config = None
        # import ipdb; ipdb.set_trace()

    def chdir(self):
        # chdir to the configured path before loading,
        # default is the current dir
        os.chdir(self.cfg.chdir)

        # add the path to sys.path
        sys.path.insert(0, self.cfg.chdir)

    def load(self):
        self.chdir()

        # load the app
        return util.import_app(self.app_uri)


def run():
    """\
    The ``api_hour`` command line runner for launching API-Hour with container.
    """
    from . import Application

    Application("%(prog)s [OPTIONS] [APP_MODULE]").run()


if __name__ == '__main__':
    run()
