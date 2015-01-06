http_and_ssh
=====

Start manually
--------------

In this current folder, launch: `api_hour -b 0.0.0.0:8008 -b 0.0.0.0:8022 http_and_ssh:Container`

Install
-------

#. Follow pythonz install doc: https://github.com/saghul/pythonz
#. pythonz install 3.4.2
#. cd /opt
#. Git clone your app here
#. cd /opt/http_and_ssh/
#. /usr/local/pythonz/pythons/CPython-3.4.2/bin/pyvenv pyvenv
#. . pyvenv/bin/activate
#. pip install -r requirements.txt
#. cd /etc/init.d/ && ln -s /opt/http_and_ssh/etc/init.d/http_and_ssh
#. cd /etc/default/ && ln -s /opt/http_and_ssh/etc/default/http_and_ssh
#. update-rc.d http_and_ssh defaults
#. cp -a /opt/http_and_ssh/etc/http_and_ssh /etc/
#. Adapt rsyslog and lograte
#. service http_and_ssh start

To restart automatically daemon if it crashes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
#. apt-get install monit
#. cd /etc/monit/conf.d/ && ln -s /opt/http_and_ssh/etc/monit/conf.d/http_and_ssh
#. service monit restart
