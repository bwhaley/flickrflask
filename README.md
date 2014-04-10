README
======
Simple Flask application that does the following:

1. Provides a UI and an API for searching flickr for photos
2. Sends the query term and its source (api or web) to an AWS SQS queue 
3. `q_worker.py` reads the messages from the queue and inserts them in a mysql database
4. The `/showqueries` endpoint shows a list of the queries, the source, and the time it was inserted to the database
5. Provides a sentiment endpoint that uses the free 3scale API to set and retrieve the use of various search terms. This is only used to demonstrate the use of Lua embedded in Nginx configuration.

## Install 

First you'll need [Flickr API credentials](https://www.flickr.com/services/api/misc.api_keys.html), full access to an AWS SQS queue, and a database. 

1. `sudo pip install -r requirements.txt`
2. Set the env variables (see list below)
3. `db-migrate --config=simple_db_migrate/simple_db_migrate.conf`
4. `python q_worker.py >/dev/null &` Run the queue reader in the background. The output is the number of message fetched.
5. `python runserver.py` Start the flask app
6. Visit `http://localhost:5000`

## The following endpoints exist:
1. `/` The landing page
2. `/search/[term]` Search Flickr for photos matching  certain term
3. `/search/[term]/[maximum]` Same as 2. but return `[maximum]` photos
4. `/api/search/[term]` Same as 2. but return JSON
5. `/sentiment/[term]` Show the sentiment of searches for this term

## Additional features & info
The etc/ directory contains configurations for apache httpd, nginx, haproxy, uwsgi, and other components of a web app stack to demonstrate features of each. The intent is to show how to operate a more complex web application using a simple app as an example.


This repository is referenced heavily in the Linux Web Operations LiveLessons video series.

### Environment Variables

|Variable                        | Description
--------------------------------|-----------------
|`AWS_ACCESS_KEY_ID`             | AWS Access Key
|`AWS_SECRET_ACCESS_KEY`         | AWS Access Key
|`AWS_REGION`                    | AWS region (us-east-1, us-west-2, etc)
|`QUEUE_URL`                     | SQS Queue URL (https://...)
|`FLICKR_KEY`                    | Flickr API Key
|`FLICKR_SECRET`                 | Flickr API Secret
|`DATABASE_HOST`                 | Database hostname or IP address
|`DATABASE_NAME`                 | Name of database (flickrflask is a good choice)
|`DATABASE_USERNAME`             | Root username for the db. Only used for DB setup
|`DATABASE_PASSWORD`             | Root password, also only used for DB setup
|`WRITER_USERNAME`               | A username to write to the DB, used by the q_worker
|`WRITER_PASSWORD`               | A password to write to the DB, used by the q_worker
|`READER_USERNAME`               | A username to read from the DB, used by the query interface
|`READER_PASSWORD`               | A password to read from the DB, used by the query interface


