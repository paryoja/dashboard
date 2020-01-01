FROM yj0604park/general:18.04
MAINTAINER Yoonjae Park <yj0604.park@gmail.com>

#COPY sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y --fix-missing python3 python3-pip postgresql-client-common postgresql-client

ADD requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install --ignore-installed -r requirements.txt

ENV PYTHONIOENCODING utf-8
RUN echo alias python="python3" >> /root/.bashrc
