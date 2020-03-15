#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

export PYTHONIOENCODING=utf-8

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput

mkdir -p logs

gunicorn dashboard.wsgi:application --bind 0.0.0.0:8000
