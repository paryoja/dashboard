#!/bin/bash
export PYTHONIOENCODING=utf-8

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

mkdir -p logs
gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000