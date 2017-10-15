import hashlib
import logging
import connexion
import requests
import json


# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')
token = ''


def login():
    username = 'admin'
    password = 'admin'

    sha = hashlib.sha1()
    sha.update(password)

    payload = {"username": username, "password": sha.hexdigest()}
    # payload = {"username": 'user1', "password": 'abcxyz'}
    r = requests.post("http://localhost:5001/auth", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    # r = requests.post("http://localhost:5001/auth", data=json.dumps(payload),
    #                   headers={'Authorization': 'token'})
    global token
    token = json.loads(r.content)['access_token']
    print token
    return json.loads(r.content)['access_token']


def protected():
    # payload = {'playlist_id': 2}
    # r = requests.get("http://localhost:5002/getPlaylistSongs", params=payload)
    #
    # songs = []
    # a = json.loads(r.content)
    # for p in a:
    #     songs.append(p)
    #
    # payload = {'songs': songs}
    # r = requests.get("http://localhost:5001/getPlaylistSongs", params=payload)

    # ******************************************************************************************************
    # ******************************************************************************************************

    # payload = {'song_id': 1, 'playlist_id': 2}
    # r = requests.post("http://localhost:5002/postSongPlaylist",
    #                   data=payload)

    payload = {'playlist_id': 2}
    r = requests.post("http://localhost:5002/delPlaylist",
                      data=payload)

    return ''


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app


# config
application.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)


if __name__ == '__main__':
    app.run(port=5003)
