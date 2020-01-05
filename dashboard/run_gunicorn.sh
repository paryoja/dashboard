#!/bin/bash
export PYTHONIOENCODING=utf-8

python3 manage.py makemigrations
python3 manage.py migrate
echo yes | python3 manage.py collectstatic

gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000