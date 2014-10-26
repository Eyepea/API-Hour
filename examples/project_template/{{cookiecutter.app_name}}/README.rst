{{cookiecutter.app_name}}
=====

Install
-------

Follow pythonz install doc
pythonz install 3.4.2
cd /opt
# Git clone your app here
cd /opt/{{cookiecutter.app_name}}/
/usr/local/pythonz/pythons/CPython-3.4.2/bin/pyvenv pyvenv
. pyvenv/bin/activate
pip install -r requirements.txt
cd /etc/init.d/ && ln -s /opt/{{cookiecutter.app_name}}/etc/init.d/{{cookiecutter.app_name}}
cd /etc/default/ && ln -s /opt/{{cookiecutter.app_name}}/etc/default/{{cookiecutter.app_name}}
cd /etc/monit/conf.d/ && ln -s /opt/{{cookiecutter.app_name}}/etc/monit/conf.d/{{cookiecutter.app_name}}
update-rc.d {{cookiecutter.app_name}} defaults
cp -a /opt/{{cookiecutter.app_name}}/etc/{{cookiecutter.app_name}} /etc/
Adapt rsyslog and lograte

service {{cookiecutter.app_name}} start
service nginx reload
service monit restart
