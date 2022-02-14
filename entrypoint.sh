#!/bin/sh


python manage.py makemigrations --no-input
python manage.py migrate --no-input

celery -A core worker -l info

celery -A core worker -l info -B

gunicorn core.wsgi --bind 0.0.0.0:$PORT




