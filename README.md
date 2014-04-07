README
======
Example Flask application that does the following:

1. Provides a UI and an API for searching flickr for photos
2. Puts the query term and its source (api or web) in an AWS SQS queue 
3. `q_worker.py` reads the messages from the queue and puts them in a mysql database
4. The `/showqueries` endpoint shows a list of the queries, the source, and the time it was inserted to the database

## Install 

First you'll need [Flickr API credentials](https://www.flickr.com/services/api/misc.api_keys.html), full access to an AWS SQS queue, and a database. 

1. `sudo pip install -r requirements.txt`
2. Set the env variables defined in `runserver.py`
 - `AWS_ACCESS_KEY_ID`
 - `AWS_SECRET_ACCESS_KEY`
 - `QUEUE_URL`
 - `AWS_REGION`
 - `FLICKR_KEY`
 - `FLICKR_SECRET`
 - `DATABASE_HOST`
 - `DATABASE_USERNAME`
 - `DATABASE_PASSWORD`
 - `DATABASE_NAME`
4. `python create_db.py` Set up the database
5. `python q_worker.py >/dev/null &` Run the queue reader in the background. The output is the number of message fetched.
7. `python runserver.py` Start the flask app
6. Visit http://localhost:5000

## The following endpoints exist:
1. /
2. /search/[term]
3. /search/[term]/[maximum]
4. /api/search/[term]

