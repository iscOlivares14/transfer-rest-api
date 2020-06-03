FROM ubuntu:18.04


# https://github.com/hellt/nginx-uwsgi-flask-alpine-docker
LABEL maintainer "Tiernan Kennedy <tiernan@beatha.io>"
LABEL description "Nginx + uWSGI + Flask based on Ubuntu 16.04 and managed by Supervisord"

# Copy python requirements file
COPY requirements.txt /tmp/requirements.txt

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev vim \
  build-essential libssl-dev libffi-dev jq \
  uwsgi nginx uwsgi-plugin-python3 supervisor \
  && python3 -m pip install --upgrade pip \
  && python3 -m pip install -r /tmp/requirements.txt

# to add nginx user
RUN adduser --disabled-password --gecos '' nginx

# Copy the Nginx global conf
COPY dockerconf/nginx.conf /etc/nginx/

# Copy the Flask Nginx site conf
COPY dockerconf/flask-site-nginx.conf /etc/nginx/conf.d/

# Copy the base uWSGI ini file to enable default dynamic uwsgi process number
COPY dockerconf/uwsgi.ini /etc/uwsgi/

# Custom Supervisord config
COPY dockerconf/supervisord.conf /etc/supervisord.conf

# Add demo app
COPY ./ /app
WORKDIR /app

EXPOSE 80

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]


