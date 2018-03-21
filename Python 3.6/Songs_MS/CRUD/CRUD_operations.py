import logging
from CRUD.ORM import db
from sqlalchemy import or_
from CRUD.entities.Song import Song


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- BASE STUFF ----------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def commit():
    logging.debug("{CRUD_operations} BEGIN function commit()")
    db.session.commit()
    logging.info("{CRUD_operations} Performed COMMIT to the database")


def rollback():
    logging.debug("{CRUD_operations} BEGIN function rollback()")
    db.session.rollback()
    logging.info("{CRUD_operations} Performed ROLLBACK to the database")


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- CREATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def create_song(title, artist, album, release_year, path, user_id):
    logging.debug('{CRUD_operations} BEGIN function create_song()')
    logging.debug('{CRUD_operations} Data received: title: %s, artist: %s, album: %s, release_year: %s, path: '
                  '%s, user_id: %s', title, artist, album, release_year, path, user_id)
    song = Song(title=title, artist=artist, album=album, release_year=release_year, path=path, user_id=user_id)
    db.session.add(song)
    logging.debug('{CRUD_operations} END function create_song()')
    return song


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- READ ----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def read_songs_by_user_id(user_id):
    """ Returns a list of songs based of an user id"""
    logging.debug('{CRUD_operations} BEGIN function read_songs_by_user_id()')
    logging.debug('{CRUD_operations} Data received: user_id: %s', user_id)
    songs = Song.query.filter_by(user_id=user_id).filter_by(is_deleted=False)
    logging.debug('{CRUD_operations} END function read_songs_by_user_id()')
    return songs


def read_song_by_song_id(song_id):
    """ Returns a song based on the song id"""
    logging.debug('{CRUD_operations} BEGIN function read_song_by_song_id()')
    logging.debug('{CRUD_operations} Data received: song_id: %s', song_id)
    song = Song.query.filter_by(id=song_id).first()
    logging.debug('{CRUD_operations} END function read_song_by_song_id()')
    return song


def read_songs_by_criteria(expression):
    """ Returns all songs comparing the given expression into all attribute columns"""
    logging.debug('{CRUD_operations} BEGIN function read_songs_by_criteria()')
    logging.debug('{CRUD_operations} Data received: expression: %s', expression)
    looking_for = '%{0}%'.format(expression)
    songs = Song.query.filter(or_(
        Song.title.ilike(looking_for),
        Song.artist.ilike(looking_for),
        Song.album.ilike(looking_for),
        Song.release_year.ilike(looking_for)
    ))
    logging.debug('{CRUD_operations} END function read_songs_by_criteria()')
    return songs


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- UPDATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def update_song(song, title, artist, album, release_year, path):
    logging.debug('{CRUD_operations} BEGIN function update_song()')
    logging.debug('{CRUD_operations} Data received: song: %s', song)
    if title is not '':
        song.title = title
    if artist is not '':
        song.artist = artist
    if album is not '':
        song.album = album
    if release_year is not '':
        song.release_year = release_year
    if path is not '':
        song.path = path
    logging.debug('{CRUD_operations} END function update_song()')
    return song


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- DELETE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


def delete_song(song):
    """ Fake deletes a song. Just change a variable is_deleted to True"""
    logging.debug('{CRUD_operations} BEGIN function delete_song()')
    logging.debug('{CRUD_operations} Data received: song: %s', song)
    song.is_deleted = True
    logging.debug('{CRUD_operations} END function delete_song()')
