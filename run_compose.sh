#!/bin/bash
docker-compose stop
chmod u+x dashboard/wait-for-it.sh
docker-compose up -d --build
