from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
import logging
import os
from Base import Base
from Song import Song

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# database -> !!sensitive information!!

db_host = os.environ['DATABASEADDRESS']
path = 'mysql+pymysql://root:ribeiro@'+db_host+'/Songs_MS'

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

    if not database_exists(engine.url):
        create_database(engine.url)

    logging.debug('{CRUD} Connect to database on path: %s', path)
    Base.metadata.create_all(engine)
    logging.debug('{CRUD} END function create_tables()')
    logging.info('{CRUD} Tables created')


def read_user_songs(user_id, search_all):
    logging.debug('{CRUD} BEGIN function read_user_songs()')
    connect_database()
    if search_all == 0:
        query = session.query(Song).filter_by(is_deleted=0).filter_by(user_id=user_id)
    else:
        query = session.query(Song).filter_by(user_id=user_id)

    logging.debug('{CRUD} Songs found: %s', query.count())
    songs = []
    for song in query:
        print song
        songs.append(song)
    logging.debug('{CRUD} END function read_user_songs()')
    logging.info('{CRUD} Song(s) retrieved')
    return songs


def read_song(song_id):
    logging.debug('{CRUD} BEGIN function read_song()')
    connect_database()
    logging.debug('{CRUD} Searching for id: %s', song_id)
    query = session.query(Song).filter_by(id=song_id)
    logging.debug('{CRUD} Found: %s', query.count())
    if query.count() != 0:
        logging.debug('{CRUD} Song found: %s', query[0])
        logging.debug('{CRUD} END function read_song()')
        logging.info('{CRUD} Song retrieved')
        return query[0]
    logging.debug('{CRUD} END function read_song()')
    logging.info('{CRUD} No song found')
    return None


def read_songs_criteria(title=None, artist=None):
    logging.debug('{CRUD} BEGIN function read_songs_criteria()')
    connect_database()
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


def update_song(song, title=None, artist=None, album=None, release_year=None, path=None):
    logging.debug('{CRUD} BEGIN function update_song()')
    # connect_database()
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
    return song


def update_song_owner(songs, admin_id):
    logging.debug('{CRUD} BEGIN function update_song_owner()')
    for s in songs:
        s.user_id = admin_id
    session.commit()
    logging.debug('{CRUD} END function update_song_owner()')
    logging.info('{CRUD} Song changed')


def create_song(title, artist, album, release_year, path_song, user_id):
    logging.debug('{CRUD} BEGIN function create_song()')
    connect_database()

    song = Song(title, artist, album, release_year, path_song, user_id)
    # song.user = user
    logging.debug('{CRUD} Creating song: %s by user: %s', title, user_id)
    session.add(song)
    session.commit()

    logging.debug('{CRUD} END function create_song()')
    logging.info('{CRUD} Song created')


def delete_song(song):
    logging.debug('{CRUD} BEGIN function delete_song()')
    logging.debug('{CRUD} Deleting %s', song)
    song.is_deleted = True
    session.commit()
    logging.debug('{CRUD} END function delete_song()')
    logging.info('{CRUD} Song deleted')