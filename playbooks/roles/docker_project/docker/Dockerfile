FROM ubuntu
MAINTAINER Lalit Sharma
RUN apt-get update
RUN apt-get install -y nginx vim curl
COPY index.html /var/www/html/index.html
EXPOSE 80/tcp
ENTRYPOINT service nginx restart && bash
