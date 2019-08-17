FROM ubuntu:18.04
MAINTAINER Yoonjae Park <yj0604.park@gmail.com>

RUN apt-get update
RUN apt-get dist-upgrade -y
RUN apt-get install -y python3 python3-pip

ADD requirements.txt .
RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requirements.txt

RUN echo alias python="python3" >> /root/.bashrc
