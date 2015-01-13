With The Starter Kit
====================

If you haven't already installed **API-Hour**, you can follow the :ref:`installation` instructions.


Generate
--------

::

    pip install cookiecutter
    cookiecutter https://github.com/Eyepea/cookiecutter-API-Hour.git

Customize
---------

| In the Starter Kit, the main file is **app_name/__init__.py**
| you will have an example using PostgreSQL, you can remove the call to aiopg if it is'nt needed.

You have all details about the directories created by cookiecutter in :ref:`container_architecture`.

Launch
------

::

    api_hour -ac app_name:Container

**-ac** is used to find the *etc/app_name* configuration directory you have in your daemon example.

You can define the configuration directory with **--config_dir** command line parameter.

For other options, type **api_hour -h** or check `Gunicorn settings documentation <http://gunicorn-docs.readthedocs.org/en/latest/settings.html>`_.
