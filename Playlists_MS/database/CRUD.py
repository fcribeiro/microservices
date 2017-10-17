from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
from Base import Base
from Playlist import Playlist
from Playlist_Song import PlaylistSongs

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# database -> !!sensitive information!!
path = 'mysql+pymysql://root:ribeiro@localhost:3306/Playlists_MS'

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


def create_playlist(name, user_id):
    logging.debug('{CRUD} BEGIN function create_playlist()')
    playlist = Playlist(name, user_id)
    logging.debug('{CRUD} Creating playlist: %s by user: %s', playlist, user_id)
    session.add(playlist)
    session.commit()
    logging.debug('{CRUD} END function create_playlist()')
    logging.info('{CRUD} Playlist created')


def add_song_playlist(playlist_id, song_id):
    playlistSong = PlaylistSongs(playlist_id, song_id)
    session.add(playlistSong)
    session.commit()


def search_song_playlist(playlist_id, song_id):
    query = session.query(PlaylistSongs).filter_by(playlist_id=playlist_id).filter_by(song_id=song_id)
    songs = []
    for song in query:
        print song
        songs.append(song)
    if len(songs) == 0:
        return True
    else:
        return False


def read_playlist_songs(playlist_id):
    logging.debug('{CRUD} BEGIN function read_playlist_songs()')
    logging.debug('{CRUD} Searching for id: %s', playlist_id)
    query = session.query(PlaylistSongs).filter_by(playlist_id=playlist_id)
    logging.debug('{CRUD} Found: %s', query.count())
    songs = []
    for song in query:
        print song
        songs.append(song)
    logging.debug('{CRUD} END function read_playlist_songs()')
    return songs


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


def read_user_playlists(user_id):
    logging.debug('{CRUD} BEGIN function read_user_playlists()')
    logging.debug('{CRUD} Searching for id: %s', user_id)
    query = session.query(Playlist).filter_by(user_id=user_id)
    logging.debug('{CRUD} Found: %s', query.count())
    playlists = []
    for playlist in query:
        playlists.append(playlist)
    if playlists:
        logging.debug('{CRUD} END function read_user_playlists()')
        logging.info('{CRUD} Playlists retrieved')
        return playlists
    logging.debug('{CRUD} END function read_user_playlists()')
    logging.info('{CRUD} No playlist found')
    return None


def update_playlist(playlist_id, name=None, size=None):
    logging.debug('{CRUD} BEGIN function update_playlist()')
    logging.debug('{CRUD} ID %s', playlist_id)
    playlist = read_playlist(playlist_id)
    if playlist is not None:
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
