FROM yj0604park/general:18.04
MAINTAINER Yoonjae Park <yj0604.park@gmail.com>

# COPY sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y --fix-missing python3 python3-pip postgresql-client-common postgresql-client
RUN apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false
RUN rm -rf /var/lib/apt/lists/*

ADD ./requirements /requirements
RUN python3 -m pip install --upgrade pip setuptools
ADD ./requirements.txt /
RUN python3 -m pip install --ignore-installed -r /requirements.txt

ADD ./scripts /scripts
RUN chmod +x /scripts/*

COPY ./dockerfiles/production/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

RUN echo alias python="python3" >> /root/.bashrc
WORKDIR /work/dashboard

ENTRYPOINT ["/entrypoint"]
