FROM ubuntu:16.04

MAINTAINER popiko
RUN apt-get update -y && \
   apt-get install -y python3 python3-pip python3-dev
RUN pip3 install uwsgi
RUN mkdir /opt/flask_app
WORKDIR /opt/flask_app
ADD requirements.txt /opt/flask_app/
RUN pip3 install -r requirements.txt
ADD . /opt/flask_app
ENTRYPOINT [ "python3" ]
CMD [ "run.py" ]
