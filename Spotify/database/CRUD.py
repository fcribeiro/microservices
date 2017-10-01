from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import hashlib
import requests
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
    logging.debug('{CRUD} Checking for admin..')
    user = read_user(email='admin')
    if user is None:
        logging.debug('{CRUD} Admin not found!!')
        sha = hashlib.sha1()
        sha.update('admin')
        create_user('admin', 'admin', sha.hexdigest())
        logging.debug('{CRUD} Admin created')
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


# def create_song(title, artist, album, release_year, path_song, user_id):
#     logging.debug('{CRUD} BEGIN function create_song()')
#
#     payload = {'title': title, 'artist': artist, 'album': album, 'release_year': release_year, 'path_song': path_song, 'user_id': user_id}
#
#     r = requests.post(songs_mservice+"/createSong", data=payload)
#
#     logging.debug('{CRUD} Creating song: %s by user: %s', title, user_id)
#     logging.debug('{CRUD} END function create_song()')
#     logging.info('{CRUD} Song uploaded')


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


# def read_song(id):
#     logging.debug('{CRUD} BEGIN function read_song()')
#     logging.debug('{CRUD} Searching for id: %s', id)
#     query = session.query(Song).filter_by(id=id)
#     logging.debug('{CRUD} Found: %s', query.count())
#     if query.count() != 0:
#         logging.debug('{CRUD} Song found: %s', query[0])
#         logging.debug('{CRUD} END function read_song()')
#         logging.info('{CRUD} Song retrieved')
#         return query[0]
#     logging.debug('{CRUD} END function read_song()')
#     logging.info('{CRUD} No song found')
#     return None


# def read_all_songs():
#     logging.debug('{CRUD} BEGIN function read_all_songs()')
#     query = session.query(Song).filter_by(is_deleted=0)
#     logging.debug('{CRUD} Songs found: %s', query.count())
#     songs = []
#     for song in query:
#         songs.append(song)
#     logging.debug('{CRUD} END function read_all_songs()')
#     logging.info('{CRUD} Song(s) retrieved')
#     return songs


def read_songs_criteria(title=None, artist=None):
    logging.debug('{CRUD} BEGIN function read_songs_criteria()')
    query = None
    if title is not None and artist is not None:
        logging.debug('{CRUD} Searching for title and artist: %s, %s', title, artist)
        query = session.query(Song).filter_by(title=title).filter_by(artist=artist).filter_by(is_deleted=False)
    elif title is None and artist is None:
        logging.debug('{CRUD} Searching for all songs!!')
        query = session.query(Song).filter_by(is_deleted=False)
    else:
        if title is not None:
            logging.debug('{CRUD} Searching for title: %s', title)
            query = session.query(Song).filter_by(title=title).filter_by(is_deleted=False)
        if artist is not None:
            logging.debug('{CRUD} Searching for artist: %s', artist)
            query = session.query(Song).filter_by(artist=artist).filter_by(is_deleted=False)
    logging.debug('{CRUD} Songs found: %s', query.count())
    songs = []
    for song in query:
        songs.append(song)
    logging.debug('{CRUD} END function read_songs_criteria()')
    logging.info('{CRUD} Song(s) retrieved')
    return songs


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


def update_song(song, title=None, artist=None, album=None, release_year=None, path=None):
    logging.debug('{CRUD} BEGIN function update_song()')
    logging.debug('{CRUD} Before %s', song)
    if title is not None:
        logging.debug('{CRUD} Changing title: %s', title)
        song.title = title
    if artist is not None:
        logging.debug('{CRUD} Changing artist: %s', artist)
        song.artist = artist
    if album is not None:
        logging.debug('{CRUD} Changing album: %s', album)
        song.album = album
    if release_year is not None:
        logging.debug('{CRUD} Changing release year: %s', release_year)
        song.release_year = release_year
    if path is not None:
        logging.debug('{CRUD} Changing path: %s', path)
        song.path = path
    session.commit()
    logging.debug('{CRUD} After %s', song)
    logging.debug('{CRUD} END function update_song()')
    logging.info('{CRUD} Song changed')


# DELETE
def delete_something(stuff):
    logging.debug('{CRUD} BEGIN function delete_something()')
    logging.debug('{CRUD} Deleting %s', stuff)
    session.delete(stuff)
    session.commit()
    logging.debug('{CRUD} END function delete_something()')
    logging.info('{CRUD} %s deleted', stuff.__class__.__name__)


# def delete_song(song):
#     logging.debug('{CRUD} BEGIN function delete_song()')
#     logging.debug('{CRUD} Deleting %s', song)
#     song.is_deleted = True
#     session.commit()
#     logging.debug('{CRUD} END function delete_song()')
#     logging.info('{CRUD} Song deleted')
