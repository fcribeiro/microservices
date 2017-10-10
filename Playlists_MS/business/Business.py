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
    logging.debug('{Business} END function post_playlist()')


def get_user_playlists(asc):
    logging.debug('{Business} BEGIN function get_user_playlists()')
    try:
        payload = decode()
    except jwt.InvalidTokenError:
        return 'ERROR', 401

    playlists = CRUD.read_user_playlists(payload['identity'])

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
    app.run(port=5005)
