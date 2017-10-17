import jwt
from flask import request
from database import *
import logging
import connexion


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

    encoded = request.headers.get('Authorization').split(' ')[1]
    payload = jwt.decode(encoded, secret, algorithms=algorithm, options=options)

    return payload


def post_playlist(name):
    logging.debug('{Business} BEGIN function post_playlist()')

    try:
        payload = decode()
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    CRUD.create_playlist(name, payload['identity'])
    # CRUD.add_song_playlist(2, 1)
    # CRUD.add_song_playlist(2, 2)
    # CRUD.add_song_playlist(3, 2)
    logging.debug('{Business} END function post_playlist()')


def post_song_playlist(playlist_id, song_id):
    logging.debug('{Business} BEGIN function post_song_playlist()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401
    if CRUD.search_song_playlist(playlist_id, song_id):
        CRUD.add_song_playlist(song_id, playlist_id)
        playlist = CRUD.read_playlist(playlist_id)
        CRUD.update_playlist(playlist_id=playlist_id, size=playlist.size+1)

    logging.debug('{Business} END function post_song_playlist()')


def get_user_playlists(asc):
    logging.debug('{Business} BEGIN function get_user_playlists()')
    try:
        payload = decode()
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    playlists = CRUD.read_user_playlists(payload['identity'])

    if playlists == None:
        return '', 400

    logging.debug('{Business} Asc: %s', asc)
    if asc == "1":
        playlists.sort(key=lambda x: x.name, reverse=False)
    if asc == "2":
        playlists.sort(key=lambda x: x.name, reverse=True)
    if asc == "3":
        playlists.sort(key=lambda x: x.size, reverse=False)
    if asc == "4":
        playlists.sort(key=lambda x: x.size, reverse=True)
    if asc == "5":
        playlists.sort(key=lambda x: x.creation_date, reverse=False)
    if asc == "6":
        playlists.sort(key=lambda x: x.creation_date, reverse=True)
    logging.debug('{Business} END function get_user_playlists()')
    logging.info('{Business} Playlists retrieved')
    return [p.dump() for p in playlists]


def get_playlist(playlist_id):
    logging.debug('{Business} BEGIN function get_playlist()')
    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    playlist = CRUD.read_playlist(playlist_id)
    print playlist
    logging.debug('{Business} END function get_playlist()')
    return playlist.dump()


def get_playlist_songs(playlist_id):
    logging.debug('{Business} BEGIN function get_playlist()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    playlist_songs = CRUD.read_playlist_songs(playlist_id)

    logging.debug('{Business} END function get_playlist()')

    return [p.dump()['song_id'] for p in playlist_songs]


def put_playlist(playlist_id, name):
    logging.debug('{Business} BEGIN function put_playlist()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    CRUD.update_playlist(playlist_id=playlist_id, name=name)

    logging.debug('{Business} END function put_playlist()')

    return 'Success', 200


def del_playlist(playlist_id):
    logging.debug('{Business} BEGIN function put_playlist()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    playlist_songs = CRUD.read_playlist_songs(playlist_id)

    for pSongs in playlist_songs:
        print 'deleting song: %s', pSongs
        CRUD.delete_something(pSongs)
    playlist = CRUD.read_playlist(playlist_id)

    CRUD.delete_something(playlist)

    logging.debug('{Business} END function put_playlist()')

    return 'Success', 200


def del_user_playlists():
    logging.debug('{Business} BEGIN function put_playlist()')

    try:
        payload = decode()
        print payload
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    user_playlists = CRUD.read_user_playlists(payload['identity'])

    for p in user_playlists:
        playlist_id = p.dump()['id']
        playlist_songs = CRUD.read_playlist_songs(playlist_id)
        for pSongs in playlist_songs:
            print 'deleting song: %s', pSongs
            CRUD.delete_something(pSongs)
        CRUD.delete_something(p)

    logging.debug('{Business} END function put_playlist()')
    return 'Success', 200


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

application.config['SECRET_KEY'] = 'super-secret'
app.debug = True

# starting database
CRUD.create_tables()
CRUD.connect_database()


if __name__ == '__main__':
    app.run(port=5002)
