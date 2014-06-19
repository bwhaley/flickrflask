FROM flickr_base
MAINTAINER Ben Whaley "ben@anki.com"

# Copy over the source
ADD . /flickrflask

# Install python dependencies
RUN /usr/local/bin/pip install -r /flickrflask/requirements.txt

# Start supervisor in the foreground
CMD ["supervisord -n"]
