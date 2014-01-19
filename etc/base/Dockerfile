FROM ubuntu:12.04
MAINTAINER Ben Whaley "ben@anki.com"
# Add universe for nginx, uwsgi, supervisor
RUN sed -i 's/main$/main universe/' /etc/apt/sources.list
RUN apt-get install -y -q software-properties-common python-software-properties
RUN apt-get -y update

# install needed packages
RUN apt-get install -y -q supervisor python-dev libxml2-dev libxslt-dev python-setuptools rsyslog libmysqlclient-dev
RUN easy_install pip
RUN easy_install -U distribute

Add requirements.txt /tmp/requirements.txt

# Install python dependencies
RUN /usr/local/bin/pip install -r /tmp/requirements.txt

