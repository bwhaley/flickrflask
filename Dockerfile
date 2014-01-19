FROM flickr_base
MAINTAINER Ben Whaley "ben@anki.com"

RUN pip install uwsgi

### nginx config
# remove default site
RUN rm /etc/nginx/sites-enabled/default
# disable daemon - supervisord will run nginx
RUN sed -i '1i daemon off;' /etc/nginx/nginx.conf

# copy the nginx config
ADD ./etc/nginx/flickr.conf /etc/nginx/sites-enabled/flickr.conf

# copy the supervisor config
ADD ./etc/supervisor/flickr.conf /etc/supervisor/conf.d/flickr.conf
ADD ./etc/supervisor/nginx.conf /etc/supervisor/conf.d/nginx.conf

# Copy over the source
ADD . /flickrdemo

# Install python dependencies
RUN /usr/local/bin/pip install -r /flickrdemo/requirements.txt
