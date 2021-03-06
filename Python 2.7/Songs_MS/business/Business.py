import jwt
from flask import request
from database import *
from sqlalchemy import exc
import logging
import connexion
import time


# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

secret = 'super-secret'
algorithm = 'HS256'


def decode():
    options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': True,
        'verify_iat': True,
        'verify_aud': True,
        'require_exp': False,
        'require_iat': False,
        'require_nbf': False
    }

    # encoded = request.headers.get('Authorization').split(' ')[1]
    encoded = request.headers.get('Authorization')
    if encoded is None:
        print('No Authorization Header')
    else:
        encoded = encoded.split(' ')[1]
    payload = jwt.decode(encoded, secret, algorithms=algorithm, options=options)

    return payload


def get_user_songs():
    logging.debug('{Business} BEGIN function get_user_songs()')

    try:
        payload = decode()
        # print payload
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    songs = CRUD.read_user_songs(user_id=payload['identity'], search_all=0)

    logging.debug('{Business} END function get_user_songs()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]


def get_playlist_songs():
    logging.debug('{Business} BEGIN function get_playlist_songs()')
    try:
        decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    songs = request.json
    final_songs = []
    for song_id in songs:
        r = CRUD.read_song(song_id)
        if r:
            final_songs.append(r)
    logging.debug('{Business} END function get_playlist_songs()')
    return [p.dump() for p in final_songs]


def get_song(song_id):
    logging.debug('{Business} BEGIN function get_song()')

    try:
        decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    song = CRUD.read_song(song_id)
    logging.debug('{Business} END function get_song()')
    logging.info('{Business} Song retrieved')
    return song.dump()


def get_songs_criteria(title=None, artist=None):
    logging.debug('{Business} BEGIN function get_songs_criteria()')

    try:
        decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    logging.debug('{Business} Parameters: %s, %s', title, artist)
    if title == "":
        title = None
    if artist == "":
        artist = None
    songs = CRUD.read_songs_criteria(title, artist)
    logging.debug('{Business} END function get_songs_criteria()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]


def put_song(title=None, artist=None, album=None, release_year=None, path_song=None, song_id=None):
    logging.debug('{Business} BEGIN function put_song()')

    try:
        decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    if title == "":
        title = None
    if artist == "":
        artist = None
    if album == "":
        album = None
    if release_year == "":
        release_year = None
    if path_song == "":
        path_song = None

    logging.debug('{Business} Parameters: %s, %s, %s, %s, %s', song_id, title, artist, album, release_year)
    song = CRUD.read_song(song_id)
    song = CRUD.update_song(song, title, artist, album, release_year, path_song)

    logging.debug('{Business} END function put_song()')
    logging.info('{Business} Song updated')
    return song.dump()


def post_song(title, artist, album, release_year, path_song):
    logging.debug('{Business} BEGIN function post_song()')

    try:
        payload = decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    CRUD.create_song(title, artist, album, release_year, path_song, payload['identity'])
    logging.debug('{Business} END function post_song()')


def del_song(song_id):
    logging.debug('{Business} BEGIN function del_song()')

    try:
        decode()
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    song = CRUD.read_song(song_id)
    CRUD.delete_song(song)
    logging.debug('{Business} END function del_song()')


def del_user_songs(admin_id):
    logging.debug('{Business} BEGIN function del_user_songs()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR in Authorization Header', 401

    print' ADMIN ID:'
    print admin_id
    print 'USER: '
    print payload['identity']

    songs = CRUD.read_user_songs(user_id=payload['identity'], search_all=1)
    CRUD.update_song_owner(songs=songs, admin_id=admin_id)

    logging.debug('{Business} END function del_user_songs()')


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

application.config['SECRET_KEY'] = 'super-secret'
app.debug = True

# starting database
while True:
    try:
        CRUD.create_tables()
        CRUD.connect_database()
    except exc.SQLAlchemyError:
        print 'DATABASE Exception'
        time.sleep(1)
        continue
    break


if __name__ == '__main__':
    app.run(port=5001)
