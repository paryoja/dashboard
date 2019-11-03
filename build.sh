#!/bin/bash
# cp /etc/apt/sources.list .
docker build -t yj0604park/general:dashboard .
docker push yj0604park/general:dashboard
