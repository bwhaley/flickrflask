#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
import re
import json
from flask import Flask, render_template, url_for, request, redirect, session, flash, Response
from flickr_api.auth import AuthHandler
from flickr_api import FlickrError
import flickr_api
import boto.sts
import boto.sqs
from boto.sqs.connection import SQSConnection
from boto.sqs.queue import Queue
from boto.sqs.message import Message
from sqlalchemy import *

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") 
queue_url = os.getenv("QUEUE_URL") 
region = os.getenv("AWS_REGION") 
flickr_key = os.getenv("FLICKR_KEY") 
flickr_secret = os.getenv("FLICKR_SECRET") 
db_host = db_name = os.getenv("DATABASE_HOST")
db_username = db_name = os.getenv("DATABASE_USERNAME")
db_password = db_name = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

secrets = {'api_key': flickr_key, 'api_secret': flickr_secret}
conn = boto.sqs.connect_to_region(
    region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

q = Queue(conn, queue_url)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search/<term>')
def api(term):
    flickr_api.set_keys(**secrets)
    write_to_sqs(term, "api")
    photos = flickr_api.Photo.search(tags=term, sort='date-posted-desc', per_page=10)
    j = []
    for photo in photos:
        j.append({
            'title': photo.title,
            'description': photo.title,
            'url': photo.getPhotoUrl()})
    response = Response(json.dumps({'photos': j}), status=200, mimetype='application/json')
    return response

@app.route('/search/<term>')
def search(term):
    flickr_api.set_keys(**secrets)
    write_to_sqs(term, "web")
    photos = flickr_api.Photo.search(tags=term, sort='date-posted-desc', per_page=10)
    #raise
    return render_template('photos.html', photos=photos, maximum=10, term=term)


@app.route('/search/<term>/<maximum>')
def search_max(term, maximum):
    try:
        maximum=int(maximum)
    except:
        flash("maximum must be integer, 10 results will be rendered", "error")
    flickr_api.set_keys(**secrets)
    write_to_sqs(term, "web")
    photos = flickr_api.Photo.search(tags=term, sort='date-posted-desc', per_page=maximum)
    return render_template('photos.html', photos=photos, maximum=maximum, term=term)

@app.route('/showqueries')
def show():
    engine = create_engine("mysql://{user}:{password}@{host}:3306/{name}".format(
        user=db_username,
        password=db_password,
        host=db_host,
        name=db_name,
        ))

    metadata = MetaData()
    metadata.bind = engine
    rs = engine.execute("select * from queries")
    return render_template('queries.html', queries=rs)

def write_to_sqs(query, type):
    m = Message()
    m.set_body(json.dumps({'q':query, 't': type}))
    q.write(m)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True) 
