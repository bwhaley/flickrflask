FROM ubuntu:12.04
MAINTAINER Ben Whaley "ben@anki.com"
# Add universe for nginx, uwsgi, supervisor
RUN sed -i 's/main$/main universe/' /etc/apt/sources.list
RUN apt-get install -y -q software-properties-common python-software-properties
RUN add-apt-repository -y  ppa:nginx/stable
RUN apt-get -y update

# install needed packages
RUN apt-get install -y -q nginx supervisor python-dev libxml2-dev libxslt-dev python-setuptools rsyslog libmysqlclient-dev
RUN easy_install pip
RUN easy_install -U distribute

# Install uwsgi container
RUN pip install uwsgi

Add requirements.txt /tmp/requirements.txt

# Install python dependencies
RUN /usr/local/bin/pip install -r /tmp/requirements.txt

### nginx config
# remove default site
RUN rm /etc/nginx/sites-enabled/default
# disable daemon - supervisord will run nginx
RUN sed -i '1i daemon off;' /etc/nginx/nginx.conf
# copy the nginx config
ADD ./etc/nginx/flickrflask-final.conf /etc/nginx/sites-enabled/flickrflask

# copy the supervisor config
ADD ./etc/supervisor/flickr.conf /etc/supervisor/conf.d/flickr.conf
ADD ./etc/supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

