#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
import re
from flask import Flask, render_template, url_for, request, redirect, session, flash
from flickr_api.auth import AuthHandler
from flickr_api import FlickrError
import flickr_api


app = Flask(__name__)

if os.path.exists('settings.py'):
    app.config.from_pyfile('settings.py')
    secrets = {'api_key': app.config.get('FLICKR_KEY'), 'api_secret': app.config.get('FLICKR_SECRET')}
else:
    print("copy settings-sample.py to settings.py and run again")
    sys.exit()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    """Login to flickr with read only access.After successful login redirects to
    callback url else redirected to index page
    """
    try:
        auth = AuthHandler(key=app.config['FLICKR_KEY'], secret=app.config['FLICKR_SECRET'],
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

app.run('0.0.0.0', debug=True, port=app.config['PORT']) # Dev env
