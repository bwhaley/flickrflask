import os
import time
import json
import boto.sqs
import boto.sts
from boto.sqs.message import Message
from boto.sqs.queue import Queue
from sqlalchemy import *

region = os.getenv("AWS_REGION") or None
aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID") or None
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY") or None
queue_url = os.getenv("QUEUE_URL")

db_host = db_name = os.getenv("DATABASE_HOST")
db_username = db_name = os.getenv("WRITER_USERNAME")
db_password = db_name = os.getenv("WRITER_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

conn = boto.sqs.connect_to_region(
    region,
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key)
conn = boto.sqs.connect_to_region(region)

q = Queue(conn, queue_url)

engine = create_engine("mysql://{user}:{password}@{host}:3306/{name}".format(
    user=db_username,
    password=db_password,
    host=db_host,
    name=db_name,
))

metadata = MetaData()
metadata.bind = engine
queries = Table('queries', metadata, autoload=True)


while True:
    messages = q.get_messages(10)
    print len(messages)
    for m in messages:
        query = json.loads(m.get_body())
        engine.execute(queries.insert(), query=query['q'], type=query['t'])
        q.delete_message(m)

    time.sleep(1)



