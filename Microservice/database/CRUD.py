from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from Base import Base
from Song import Song

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


def read_user_songs(userID):
    logging.debug('{CRUD} BEGIN function read_user_songs()')
    connect_database()
    query = session.query(Song).filter_by(is_deleted=0).filter_by(user_id=userID)
    logging.debug('{CRUD} Songs found: %s', query.count())
    songs = []
    for song in query:
        print song
        songs.append(song)
    logging.debug('{CRUD} END function read_user_songs()')
    logging.info('{CRUD} Song(s) retrieved')
    return songs


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
