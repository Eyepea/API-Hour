import sys

import asyncssh
from ..endpoints.ssh import MirrorSSHServerSession


class InternalSSHServer(asyncssh.SSHServer):
    def connection_made(self, conn):
        print('SSH connection received from %s.' %
              conn.get_extra_info('peername')[0])

    def connection_lost(self, exc):
        if exc:
            print('SSH connection error: ' + str(exc), file=sys.stderr)
        else:
            print('SSH connection closed.')

    def begin_auth(self, username):
        # No auth in this example
        return False

    def session_requested(self):
        # return MirrorSSHServerSession(self.ah_container)
        return MirrorSSHServerSession()
