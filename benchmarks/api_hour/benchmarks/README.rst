benchmarks
=====

Start manually
--------------

In this current folder, launch: **api_hour benchmarks:Container**

Install
-------

Follow pythonz install doc: https://github.com/saghul/pythonz
pythonz install 3.4.2
cd /opt
# Git clone your app here
cd /opt/benchmarks/
/usr/local/pythonz/pythons/CPython-3.4.2/bin/pyvenv pyvenv
. pyvenv/bin/activate
pip install -r requirements.txt
cd /etc/init.d/ && ln -s /opt/benchmarks/etc/init.d/benchmarks
cd /etc/default/ && ln -s /opt/benchmarks/etc/default/benchmarks
cd /etc/monit/conf.d/ && ln -s /opt/benchmarks/etc/monit/conf.d/benchmarks
update-rc.d benchmarks defaults
cp -a /opt/benchmarks/etc/benchmarks /etc/
Adapt rsyslog and lograte

service benchmarks start
service nginx reload
service monit restart
