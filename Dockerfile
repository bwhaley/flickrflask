FROM flickr_base
MAINTAINER Ben Whaley "ben@anki.com"

RUN apt-get install -y -q nginx supervisor python-dev libxml2-dev libxslt-dev python-setuptools rsyslog libmysqlclient-dev

# Install uwsgi container
RUN pip install uwsgi

# copy the supervisor config
ADD ./etc/supervisor/flickr.conf /etc/supervisor/conf.d/flickr.conf

# Copy over the source
ADD . /flickrdemo

# Install python dependencies
RUN /usr/local/bin/pip install -r /flickrdemo/requirements.txt
