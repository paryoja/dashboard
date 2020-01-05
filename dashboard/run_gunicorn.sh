#!/bin/bash
export PYTHONIOENCODING=utf-8

python3 manage.py makemigrations
python3 manage.py migrate

gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000