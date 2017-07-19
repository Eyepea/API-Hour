import os
import re
import sys
from setuptools import setup, find_packages

__docformat__ = 'rst'

PY_VER = sys.version_info[:3]

if PY_VER < (3, 5, 0):
    PY_VERS = '.'.join(map(str, PY_VER))
    raise RuntimeError("api_hour doesn't support Python earlier than 3.5.0, "
                       "current Python version is: %s" % PY_VERS)

install_requires = ['gunicorn', 'PyYAML', 'setproctitle']


def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()


def read_version():
    regexp = re.compile(r"^__version__\W*=\W*'([\d.abrc]+)'")
    init_py = os.path.join(os.path.dirname(__file__), 'api_hour', '__init__.py')
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        else:
            raise RuntimeError('Cannot find version in api_hour/__init__.py')


classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: No Input/Output (Daemon)',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: Apache Software License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
    'Topic :: System :: Networking',
]


setup(name='api_hour',
      version=read_version(),
      description=('Write efficient network daemons (HTTP, SSH...) with ease.'),
      long_description='\n\n'.join((read('README.rst'), read('HISTORY.rst'))),
      classifiers=classifiers,
      platforms=['OS Independent'],
      author='Eyepea Dev Team',
      author_email='gmludo@gmail.com',
      url='http://www.api-hour.io',
      download_url='https://pypi.python.org/pypi/api_hour',
      keywords = ['asyncio', 'performance', 'efficient', 'web', 'service', 'rest', 'json', 'daemon', 'application'],
      license='Apache 2',
      packages=find_packages(),
      install_requires=install_requires,
      # tests_require = tests_require,
      # test_suite = 'nose.collector',
      provides=['api_hour'],
      include_package_data=True,
      entry_points="""
      [console_scripts]
      api_hour=api_hour.application:run
      """,
)
