# coding=utf-8
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

db_host = db_name = os.getenv("DATABASE_HOST")
db_username = db_name = os.getenv("DATABASE_USERNAME")
db_password = db_name = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

app = Flask(__name__)
DB = "mysql://%s:%s@%s/%s" % (db_username, db_password, db_host, db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = DB
db = SQLAlchemy(app)


db.engine.execute("create table queries ( id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, query VARCHAR(256), created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP )")
