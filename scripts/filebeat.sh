#!/bin/bash

set -o errexit
set -o pipefail
set -o nounset

filebeat modules enable nginx
filebeat setup
filebeat -e