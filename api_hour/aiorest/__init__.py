import collections
import re
import sys


__version__ = '0.3.3'

version = __version__ + ' , Python ' + sys.version


VersionInfo = collections.namedtuple('VersionInfo',
                                     'major minor micro releaselevel serial')


def _parse_version(ver):
    RE = (r'^(?P<major>\d+)\.(?P<minor>\d+)\.'
          '(?P<micro>\d+)((?P<releaselevel>[a-z]+)(?P<serial>\d+)?)?$')
    match = re.match(RE, ver)
    try:
        major = int(match.group('major'))
        minor = int(match.group('minor'))
        micro = int(match.group('micro'))
        levels = {'c': 'candidate',
                  'a': 'alpha',
                  'b': 'beta',
                  None: 'final'}
        releaselevel = levels[match.group('releaselevel')]
        serial = int(match.group('serial')) if match.group('serial') else 0
        return VersionInfo(major, minor, micro, releaselevel, serial)
    except Exception:
        raise ImportError("Invalid package version {}".format(ver))


version_info = _parse_version(__version__)


from .arbiter import Arbiter
from .application import Application
from .request import Request, Response
from .errors import RESTError, JsonDecodeError, JsonLoadError
from . import serialize

# make pyflakes happy
(Arbiter, Application, Request, Response, RESTError, JsonDecodeError, JsonLoadError,
 serialize)
