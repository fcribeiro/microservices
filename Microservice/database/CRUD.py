from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import hashlib
from Base import Base
from User import User
from Song import Song
from Playlist import Playlist

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# database -> !!sensitive information!!
path = 'mysql+pymysql://root:ribeiro@localhost:3306/spotify'

session = None


def connect_database():
    logging.debug('{CRUD} BEGIN function connect_database()')
    engine = create_engine(path)
    logging.debug('{CRUD} Connect to database on path: %s', path)
    Session = sessionmaker(bind=engine)
    global session
    session = Session()
    logging.debug('{CRUD} END function connect_database()')
    logging.info('{CRUD} Connected to database')


def create_tables():
    logging.debug('{CRUD} BEGIN function create_tables()')
    engine = create_engine(path)
    logging.debug('{CRUD} Connect to database on path: %s', path)
    Base.metadata.create_all(engine)
    logging.debug('{CRUD} END function create_tables()')
    logging.info('{CRUD} Tables created')


def read_all_songs():
    logging.debug('{CRUD} BEGIN function read_all_songs()')
    query = session.query(Song).filter_by(is_deleted=False)
    logging.debug('{CRUD} Songs found: %s', query.count())
    songs = []
    for song in query:
        songs.append(song)
    logging.debug('{CRUD} END function read_all_songs()')
    logging.info('{CRUD} Song(s) retrieved')
    return songs

