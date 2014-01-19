#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
import re
import json
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flickr_api.auth import AuthHandler
from flickr_api import FlickrError
import flickr_api
import boto.sqs
from boto.sqs.queue import Queue
from boto.sqs.message import Message
from sqlalchemy import *

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID") or None
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") or None
queue_url = os.getenv("QUEUE_URL") or None
flickr_key = os.getenv("FLICKR_KEY") or None
flickr_secret = os.getenv("FLICKR_SECRET") or None
db_host = db_name = os.getenv("DATABASE_HOST")
db_username = db_name = os.getenv("DATABASE_USERNAME")
db_password = db_name = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

secrets = {'api_key': flickr_key, 'api_secret': flickr_secret}

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    """Login to flickr with read only access.After successful login redirects to
    callback url else redirected to index page
    """
    try:
        auth = AuthHandler(key=flickr_key, secret=flickr_secret,
        callback=url_for('flickr_callback', _external=True))
        return redirect(auth.get_authorization_url('read'))
    except FlickrError, f:
        # Flash failed login & redirect to index page
        flash(u'Failed to authenticate user with flickr', 'error')
        return redirect(url_for('index'))

@app.route('/login/callback')
def flickr_callback():
    """Callback handler from flickr.
    Set the oauth token, oauth_verifier to session variable for later use.
    Redirect to /photos
    """
    session['oauth_token'] = request.args.get('oauth_token')
    session['oauth_verifier'] = request.args.get('oauth_verifier')
    flash("logged in successfully", "success")
    return redirect(url_for('index'))


@app.route('/search/<term>')
def search(term):
    flickr_api.set_keys(**secrets)
    write_to_sqs(term)
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
    write_to_sqs(term)
    photos = flickr_api.Photo.search(tags=term, sort='date-posted-desc', per_page=maximum)
    return render_template('photos.html', photos=photos, maximum=maximum, term=term)


@app.route('/photos/<user>')
def photos(user):
    try:
        flickr_api.set_auth_handler(session['oauth_token'])
        flickr_api.set_keys(**secrets)
        if re.match("^[a-zA-Z0-9._%-]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$", user):
            person = flickr_api.Person.findByEmail(user)
        else:
            person = flickr_api.Person.findByUserName(user)
        photos, resp = person.getPhotos()
    except FlickrError, e:
        raise
        flash("You need to be logged in, redirecting", "error")
        return redirect(url_for('login'))
    raise

@app.route('/showqueries')
def show():
    db_host='flickrdemo.clabneqazgln.us-east-1.rds.amazonaws.com'
    db_name='flickrdemo'
    db_password='flickrdemo'
    db_username='flickr'
    engine = create_engine("mysql://{user}:{password}@{host}:3306/{name}".format(
        user=db_username,
        password=db_password,
        host=db_host,
        name=db_name,
        ))

    metadata = MetaData()
    metadata.bind = engine
    rs = engine.execute("select * from queries")
    #for row in rs:
    #    print "Query: %s" % row['query']

    return render_template('queries.html', queries=rs)

def write_to_sqs(query):
    m = Message()
    m.set_body(json.dumps({'q':query}))
    q.write(m)

conn = boto.sqs.connect_to_region(
    "us-east-1",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)

q = Queue(conn, queue_url)

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True) # Dev env

