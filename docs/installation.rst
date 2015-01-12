.. _installation:

Installation
============

Requirements
------------

If you don't have Python 3.3+ on your computer, you can install:

Ubuntu Trusty (14.04+) or Debian Jessie (8.0+)
``````````````````````````````````````````````
::

    apt-get install python3-venv python3-pip

Install API-Hour with a Pyvenv
------------------------------

| To avoid to conflict with your Python system libraries, we recommend to use Pyvenv.
| Debian package source for API-Hour is also available in `our Github repository <https://github.com/Eyepea/API-Hour>`_.

::

    pyvenv pyvenv           # This command will create a Python virtual environment named pyvenv
    . pyvenv/bin/activate   # Enable your Pyvenv
    pip install api_hour    # Install API-Hour
    pip install aiohttp     # Bonus: If you want to create a HTTP daemon

