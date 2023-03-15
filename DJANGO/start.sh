#!/bin/sh 
yes | python manage.py makemigrations --settings=drfproject.settings

echo "==> Django setup, executing: migrate pro"
python manage.py migrate --settings=drfproject.settings --fake-initial

echo "==> Django setup, executing: collectstatic"
python manage.py collectstatic --settings=drfproject.settings --noinput -v 3

pip install -r /srv/code/requirements.txt
echo "==> Django deploy"

gunicorn -b 0.0.0.0:8000 --env DJANGO_SETTINGS_MODULE=drfproject.settings drfproject.wsgi:application