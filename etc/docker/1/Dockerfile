# Start with the base Ubuntu 12.04 image
FROM ubuntu:12.04
MAINTAINER Ben Whaley "bwhaley@gmail.com"

# Patch the system
RUN apt-get -y update 

# Install pip
RUN apt-get -y install python-pip gcc python-dev

# Install uwsgi python application server
RUN pip install uwsgi

# Copy the package dependencies
ADD requirements.txt /tmp/requirements.txt

# Install python dependencies
RUN pip install -r /tmp/requirements.txt

# Clean up dependency file
RUN rm /tmp/requirements.txt
