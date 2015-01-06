import asyncssh

import http_and_ssh

class MirrorSSHServerSession(asyncssh.SSHServerSession):
    def __init__(self):
        # self.container = container
        self._chan = None

    def shell_requested(self):
        return True

    def connection_made(self, chan):
        self._chan = chan

    def session_started(self):
        self._chan.write('Welcome to my SSH server, %s!\r\nPress "q" button to leave.\r\n' %
                         self._chan.get_extra_info('username'))

    def data_received(self, data, data_type):
        self._chan.write(data)
        if data == 'q':
            self._chan.exit(0)
        # self.container.current_ssh_text += data
        http_and_ssh.CURRENT_SSH_TEXT += data