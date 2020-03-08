#!/bin/bash

set -o errexit
set -o nounset

celery flower --app=dashboard \
  --basic_auth="${CELERY_FLOWER_USER}:${CELERY_FLOWER_PASSWORD}"
