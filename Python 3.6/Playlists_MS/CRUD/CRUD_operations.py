import logging
from CRUD.ORM import db
from CRUD.entities.Playlist import Playlist
from CRUD.entities.Playlist_Song import Playlist_Song
from business.emp_zipkin_decorator import emp_zipkin_decorator


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- BASE STUFF ----------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------

@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.commit', port=5002)
def commit():
    logging.debug("{CRUD_operations} BEGIN function commit()")
    db.session.commit()
    logging.info("{CRUD_operations} Performed COMMIT to the database")


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.rollback', port=5002)
def rollback():
    logging.debug("{CRUD_operations} BEGIN function rollback()")
    db.session.rollback()
    logging.info("{CRUD_operations} Performed ROLLBACK to the database")


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- CREATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.create_playlist', port=5002)
def create_playlist(name, user_id):
    logging.debug('{CRUD_operations} BEGIN function create_playlist()')
    logging.debug('{CRUD_operations} Data received: name: %s, user_id: %s', name, user_id)
    playlist = Playlist(name=name, user_id=user_id)
    db.session.add(playlist)
    logging.debug('{CRUD_operations} END function create_playlist()')
    return playlist


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.create_song_in_playlist', port=5002)
def create_song_in_playlist(playlist_id, song_id):
    logging.debug('{CRUD_operations} BEGIN function create_song_in_playlist()')
    logging.debug('{CRUD_operations} Data received: playlist_id: %s, song_id: %s', playlist_id, song_id)
    song_in_playlist = Playlist_Song(playlist_id=playlist_id, song_id=song_id)
    db.session.add(song_in_playlist)
    logging.debug('{CRUD_operations} END function create_song_in_playlist()')
    return song_in_playlist


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- READ ----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.read_playlist_by_id', port=5002)
def read_playlist_by_id(id):
    """ Returns a playlist given an id"""
    logging.debug('{CRUD_operations} BEGIN function read_playlist_by_id()')
    logging.debug('{CRUD_operations} Data received: id: %s', id)
    playlist = Playlist.query.filter_by(id=id).first()
    logging.debug('{CRUD_operations} END function read_playlist_by_id()')
    return playlist


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.read_song_from_playlist', port=5002)
def read_song_from_playlist(playlist_id, song_id):
    """ Returns an entry playlist-song (if exists)"""
    logging.debug('{CRUD_operations} BEGIN function read_song_from_playlist()')
    logging.debug('{CRUD_operations} Data received: playlist_id: %s, song_id: %s', playlist_id, song_id)
    playlist_song = Playlist_Song.query.filter_by(playlist_id=playlist_id).filter_by(song_id=song_id).first()
    logging.debug('{CRUD_operations} END function read_song_from_playlist()')
    return playlist_song


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.read_songs_from_playlist', port=5002)
def read_songs_from_playlist(playlist_id):
    """ Returns all songs from a playlist"""
    logging.debug('{CRUD_operations} BEGIN function read_songs_from_playlist()')
    logging.debug('{CRUD_operations} Data received: playlist_id: %s', playlist_id)
    songs = Playlist_Song.query.filter_by(playlist_id=playlist_id)
    logging.debug('{CRUD_operations} END function read_songs_from_playlist()')
    return songs


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.read_all_user_playlists', port=5002)
def read_all_user_playlists(user_id):
    """ Returns all users' playlists"""
    logging.debug('{CRUD_operations} BEGIN function read_all_user_playlists()')
    logging.debug('{CRUD_operations} Data received: user_id: %s', user_id)
    playlists = Playlist.query.filter_by(user_id=user_id)
    logging.debug('{CRUD_operations} END function read_all_user_playlists()')
    return playlists


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- UPDATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.update_playlist', port=5002)
def update_playlist(playlist, name=None, size_to_add=None):
    """ Method to update a playlist name or/and size. The given number is added to the current size"""
    logging.debug('{CRUD_operations} BEGIN function update_playlist()')
    logging.debug('{CRUD_operations} Data received: playlist: %s', playlist)
    if name is not None:
        playlist.name = name
    if size_to_add is not None:
        playlist.size = playlist.size + size_to_add
    logging.debug('{CRUD_operations} END function update_playlist()')
    return playlist


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- DELETE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='playlists_ms', span_name='CRUD_operations.delete_object', port=5002)
def delete_object(entry):
    """ Method that removes any object from the database"""
    logging.debug('{CRUD_operations} BEGIN function delete_object()')
    logging.debug('{CRUD_operations} Data received: entry: %s', entry)
    db.session.delete(entry)
    logging.debug('{CRUD_operations} END function delete_object()')
