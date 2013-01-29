README
======
Demo project for accessing flickr photos using python, flask, flickr_api. [Under Construction]

1. `sudo pip install -r requirements.txt`
2. `cp settings-sample.py to settings.py`
3. Create a flickr [application][] and add `FLICKR_KEY` & `FLICKR_SECRET` to `settings.py`
4. `python runserver.py`
5. Visit http://localhost:3333

Use only following endpoints:
=====
1. /
2. /search/[term]
3. /search/[term]/[maximum]

Features
=======

1. Search Public photos with limit

[application]: http://www.flickr.com/services/apps/create/ 