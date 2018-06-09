import logging
import os
import time
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import configparser

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

config = configparser.ConfigParser()
config.read("config.ini")

DATABASE = config.get('MySQL', 'db_name')
TABLE = config.get('MySQL', 'table')
USER = config.get('MySQL', 'user')
PASSWORD = config.get('MySQL', 'password')
HOST = os.environ['DATABASEADDRESS']


# app is the object for flask managent
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % (USER, PASSWORD, HOST, DATABASE)
# db is now our orm manager
db = SQLAlchemy(app)

from CRUD.entities import Playlist_Song, Playlist

logging.debug("{ORM} Connecting into database ...")
while True:
    try:
        url = 'mysql+pymysql://%s:%s@%s' % (USER, PASSWORD, HOST)
        engine = create_engine(url)
        query = "CREATE DATABASE IF NOT EXISTS %s ;" % DATABASE
        engine.execute(query)
        db.create_all()
        db.session.commit()
    except Exception:
        logging.debug("{ORM} Database is down. Reconnecting in 5 seconds ....")
        time.sleep(5)
        continue
    break



