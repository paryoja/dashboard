#!/bin/bash
pwd=$(pwd)
docker run --rm -it --network=dashboard_default --name=django -v "$pwd":/work dashboard_django /bin/bash
