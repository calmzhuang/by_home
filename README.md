# by_home
# python manage.py runsslserver 0.0.0.0:8100 --certificate .pem --key .key
uwsgi --ini uwsgi.ini
uwsgi --reload uwsgi.pid
uwsgi --stop uwsgi.pid

/usr/sbin/nginx -s reload
