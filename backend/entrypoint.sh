#!/bin/sh

python -m pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn core.wsgi:application --bind 0.0.0.0:6500