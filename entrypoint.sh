#!/bin/bash
printenv > /etc/environment
cd /
sleep 10
python manage.py migrate
uwsgi --ini uwsgi.ini
if [ "$DEBUG" == "False" ]
then
  python manage.py collectstatic --noinput
fi

if [[ ! -v DJANGO_SETTINGS_MODULE ]]; then
    export DJANGO_SETTINGS_MODULE="Moocshop.settings"
fi

echo "Launching Entrypoint with $DJANGO_SETTINGS_MODULE"

# Cronmanager uwsgi
uwsgi -d /dev/null --chdir=./ --module=Moocshop.wsgi:application --env DJANGO_SETTINGS_MODULE=Moocshop.settings \
--master --pidfile=/tmp/project-master-cron.pid --http=0.0.0.0:8001 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum

# Django main uwsgi
uwsgi --chdir=./ --module=Moocshop.wsgi:application --env DJANGO_SETTINGS_MODULE=Moocshop.settings \
--master --pidfile=/tmp/project-master.pid --http=0.0.0.0:8000 --processes=5 \
--harakiri=20 --max-requests=5000 --vacuum
