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


# CREATE
def create_user(name, email, password):
    logging.debug('{CRUD} BEGIN function create_user()')
    logging.debug('{CRUD} Name: %s', name)
    logging.debug('{CRUD} Email: %s', email)
    logging.debug('{CRUD} Password: %s', password)
    user = User(name, email, password)
    logging.debug('{CRUD} Creating user: %s', user)
    session.add(user)
    session.flush()
    session.commit()
    logging.debug('{CRUD} END function create_user()')
    logging.info('{CRUD} User created')


def create_playlist(user, name):
    logging.debug('{CRUD} BEGIN function create_playlist()')
    playlist = Playlist(name)
    playlist.user = user
    logging.debug('{CRUD} Creating playlist: %s by user: %s', playlist, user)
    session.add(playlist)
    session.commit()
    logging.debug('{CRUD} END function create_playlist()')
    logging.info('{CRUD} Playlist created')


# READ
def read_user(email=None, id=None, password=None):
    logging.debug('{CRUD} BEGIN function read_user()')
    query = None
    if password is not None:
        logging.debug('{CRUD} Searching for email: %s', email)
        query = session.query(User).filter_by(email=email)
        logging.debug('{CRUD} Found: %s', query.count())
        if query.count() != 0:
            user = query[0]
            logging.debug('{CRUD} Comparing passwords: %s vs %s', password, user.password)
            if password == user.password:
                logging.debug('{CRUD} END function read_user()')
                logging.info('{CRUD} User retrieved!!')
                return user
            logging.debug('{CRUD} Passwords dont match!!')
        logging.debug('{CRUD} END function read_user()')
        logging.info('{CRUD} No user found')
        return None
    if email is not None:
        logging.debug('{CRUD} Searching for email: %s', email)
        query = session.query(User).filter_by(email=email)
    if id is not None:
        logging.debug('{CRUD} Searching for id: %s', id)
        query = session.query(User).filter_by(id=id)
    logging.debug('{CRUD} Found: %s', query.count())
    if query.count() != 0:
        logging.debug('{CRUD} User found: %s', query[0])
        logging.debug('{CRUD} END function read_user()')
        logging.info('{CRUD} User retrieved')
        return query[0]
    logging.debug('{CRUD} END function read_user()')
    logging.info('{CRUD} No user found')
    return None


def read_playlist(id):
    logging.debug('{CRUD} BEGIN function read_playlist()')
    logging.debug('{CRUD} Searching for id: %s', id)
    query = session.query(Playlist).filter_by(id=id)
    logging.debug('{CRUD} Found: %s', query.count())
    if query.count() != 0:
        logging.debug('{CRUD} Playlist found: %s', query[0])
        logging.debug('{CRUD} END function read_playlist()')
        logging.info('{CRUD} Playlist retrieved')
        return query[0]
    logging.debug('{CRUD} END function read_playlist()')
    logging.info('{CRUD} No playlist found')
    return None


# UPDATE
def update_user(user, name=None, email=None, password=None):
    logging.debug('{CRUD} BEGIN function update_user()')
    logging.debug('{CRUD} Before %s', user)
    if name is not None:
        logging.debug('{CRUD} Changing name: %s', name)
        user.name = name
    if email is not None:
        logging.debug('{CRUD} Changing email: %s', email)
        user.email = email
    if password is not None:
        logging.debug('{CRUD} Changing password: %s', password)
        user.password = password
    session.commit()
    logging.debug('{CRUD} After %s', user)
    logging.debug('{CRUD} END function update_user()')
    logging.info('{CRUD} User changed')


def update_playlist(playlist, name=None, size=None):
    logging.debug('{CRUD} BEGIN function update_playlist()')
    logging.debug('{CRUD} Before %s', playlist)
    if name is not None:
        logging.debug('{CRUD} Changing name: %s', name)
        playlist.name = name
    if size is not None:
        logging.debug('{CRUD} Changing size: %s', size)
        playlist.size = size
    session.commit()
    logging.debug('{CRUD} After %s', playlist)
    logging.debug('{CRUD} END function update_playlist()')
    logging.info('{CRUD} Playlist changed')


# DELETE
def delete_something(stuff):
    logging.debug('{CRUD} BEGIN function delete_something()')
    logging.debug('{CRUD} Deleting %s', stuff)
    session.delete(stuff)
    session.commit()
    logging.debug('{CRUD} END function delete_something()')
    logging.info('{CRUD} %s deleted', stuff.__class__.__name__)

