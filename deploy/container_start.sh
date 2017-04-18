#!/bin/sh
cd /var/projects/mtgpl && python manage.py migrate --noinput
supervisord -n -c /etc/supervisor/supervisord.conf