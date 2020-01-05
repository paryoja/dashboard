#!/bin/sh

(rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbitmq.pid; \
rabbitmqctl add_user $RABBITMQ_USER $RABBITMQ_PASSWORD; \
rabbitmqctl set_user_tags $RABBITMQ_USER administrator; \
rabbitmqctl add_vhost myvhost; \
rabbitmqctl set_permissions -p myvhost $RABBITMQ_USER  ".*" ".*" ".*";) &

# $@ is used to pass arguments to the rabbitmq-server command.
# For example if you use it like this: docker run -d rabbitmq arg1 arg2,
# it will be as you run in the container rabbitmq-server arg1 arg2
rabbitmq-server $@
