FROM ubuntu:16.04

MAINTAINER popiko

RUN mkdir /opt/vue_app
RUN apt-get update && apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get update && apt-get install -y nodejs

ADD . /opt/vue_app

WORKDIR /opt/vue_app

RUN npm install 
RUN npm run build

ENV HOST 0.0.0.0
ENV PORT 8080

EXPOSE 8080


CMD ["npm", "start" ]
