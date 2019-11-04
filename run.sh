#!/bin/bash
docker run --rm -it --network=mybridge --name=django -p 38000:8000 -v `pwd`:/work yj0604park/dashboard:latest /bin/bash
