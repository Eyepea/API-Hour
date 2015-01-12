With Starter Kit
================

If you don't already install **API-Hour**, you can follow :ref:`installation` instructions.


Generate
--------

::

    pip install cookiecutter
    cookiecutter https://github.com/Eyepea/cookiecutter-API-Hour.git

Customize
---------

| In Starter Kit, the main file is **app_name/__init__.py**
| you have an example with PostgreSQL, you can remove source code if you doesn't need that.

You have all details about directories created by cookiecutter in :ref:`container_architecture`.

Launch
------

::

    api_hour -ac app_name:Container

**-ac** means you use config discovery to find *etc/app_name* configuration directory you have in your daemon example.

You can define the configuration directory with **--config_dir** command line parameter.

For other options, type **api_hour -h** or check `Gunicorn settings documentation <http://gunicorn-docs.readthedocs.org/en/latest/settings.html>`_.