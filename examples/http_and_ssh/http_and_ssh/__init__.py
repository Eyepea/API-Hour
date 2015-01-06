import logging
import asyncio

import aiohttp.web
from asyncssh import import_private_key
from asyncssh.connection import SSHServerConnection

import api_hour

from . import endpoints
from .servers.ssh import InternalSSHServer


LOG = logging.getLogger(__name__)

CURRENT_SSH_TEXT = '' # ugly hack to share data between SSH and HTTP


class Container(api_hour.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.current_ssh_text = ''  # Text typed via SSH # Can't use that, no reference of SSHServerConnection in InternalSSHServer

        ## Servers
        # You can define several servers, to listen HTTP and SSH for example.
        # If you do that, you need to listen on two ports with api_hour --bind command line.
        self.servers['http'] = aiohttp.web.Application(loop=kwargs['loop'])
        self.servers['http'].ah_container = self # keep a reference to Container
        # routes
        self.servers['http'].router.add_route('GET',
                                              '/get_ssh_content',
                                              endpoints.http.get_ssh_content)

    def make_servers(self):
        # This method is used by api_hour command line to bind each server on each socket
        # Please don't touch if you don't understand how it works
        ssh_server = SSHServerConnection(server_factory=InternalSSHServer, loop=self.loop,
                                         server_host_keys=[import_private_key(self.config['servers']['ssh']['private_key'].encode('utf-8'),
                                                                              self.config['servers']['ssh']['passphrase'])])
        ssh_server.ah_container = self
        return [self.servers['http'].make_handler(logger=self.worker.log,
                                                  debug=self.worker.cfg.debug,
                                                  keep_alive=self.worker.cfg.keepalive,
                                                  access_log=self.worker.log.access_log,
                                                  access_log_format=self.worker.cfg.access_log_format),
                lambda: ssh_server]

    @asyncio.coroutine
    def start(self):
        yield from super().start()
        LOG.info('Starting engines...')
        LOG.info('All engines ready !')


    @asyncio.coroutine
    def stop(self):
        LOG.info('Stopping engines...')
        LOG.info('All engines stopped !')
        yield from super().stop()