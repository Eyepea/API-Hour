import os
import re
import sys
from setuptools import setup, find_packages

__docformat__ = 'rst'

install_requires = ['aiohttp>=0.9.3', 'configobj', 'ujson', 'lockfile', 'setproctitle']

PY_VER = sys.version_info

if PY_VER >= (3, 4, 2):
    pass
else:
    raise RuntimeError("api_hour doesn't support Python earlier than 3.4.2")

extras_require = {'redis_session': ['aioredis>=0.1.3']}


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
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: BSD License',
    'Natural Language :: English',
    'Natural Language :: French',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: Implementation :: CPython',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
]


setup(name='api_hour',
      version=read_version(),
      description=('Write efficient WebServices with ease.'),
      long_description='\n\n'.join((read('README.rst'), read('HISTORY.rst'))),
      classifiers=classifiers,
      platforms=['OS Independent'],
      author='Eyepea Dev Team',
      author_email='gmludo@gmail.com',
      url='http://www.api-hour.io',
      download_url='https://pypi.python.org/pypi/api_hour',
      keywords = ['asyncio', 'performance', 'efficient', 'web', 'service', 'rest', 'json'],
      license='BSD',
      packages=find_packages(),
      install_requires=install_requires,
      extras_require=extras_require,
      # tests_require = tests_require,
      # test_suite = 'nose.collector',
      provides=['api_hour'],
      # requires=['aiohttp'],
      include_package_data=True)
