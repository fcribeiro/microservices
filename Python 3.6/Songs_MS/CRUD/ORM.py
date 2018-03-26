import logging
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# TODO: Sensitive information ºº
DATABASE = 'Songs_MS'
TABLE = 'songs'
USER = 'root'
PASSWORD = 'ribeiro'
HOST = os.environ['DATABASEADDRESS']
# TODO: Sensitive information ºº


def create_database():
    logging.debug("{ORM} BEGIN function create_database()")

    try:
        logging.debug("{ORM} Checking database ...")
        url = 'mysql+pymysql://%s:%s@%s/%s' % (USER, PASSWORD, HOST, DATABASE)
        engine = create_engine(url)
        query = "SELECT * FROM %s;" % TABLE
        engine.execute(query)
        logging.debug("{ORM} Database already exists!")
    except Exception:
        url = 'mysql+pymysql://%s:%s@%s' % (USER, PASSWORD, HOST)
        engine = create_engine(url)
        query = "CREATE DATABASE IF NOT EXISTS %s ;" % DATABASE
        engine.execute(query)
        logging.debug("{ORM} Created database with success!")
        db.create_all()
        db.session.commit()
        logging.debug("{ORM} Created tables with success!")


# app is the object for flask managent
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://%s:%s@%s/%s' % (USER, PASSWORD, HOST, DATABASE)
# db is now our orm manager
db = SQLAlchemy(app)


