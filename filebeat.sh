#!/bin/bash

#chown filebeat:filebeat /etc/filebeat/filebeat.yml
#chmod 644 /etc/filebeat/filebeat.yml

filebeat modules enable nginx
filebeat setup
filebeat -e