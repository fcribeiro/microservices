import logging
import business.response_handling as RESP
import requests
import multiprocessing
import os
import json
from business.auth import requires_auth
from flask import request
import socket

SONGS_MS = "http://" + os.environ['SONGSADDRESS']
PLAYLISTS_MS = "http://" + os.environ['PLAYLISTSADDRESS']


def hello_world():
    return RESP.response_200(message='Aggregator_MS working! -> Host: ' + socket.gethostname())


@requires_auth
def get_playlist_songs_info(id):
    """ Retrieves all playlist songs' information"""
    logging.debug("{aggregator_controller} BEGIN function get_playlist_songs_info()")

    if id is '':
        return RESP.response_400(message='A given parameter is empty')

    # Checks if song exists by sending a request into the Songs Microservice
    headers = {'Content-Type': 'application/json',
               'Authorization': request.headers['Authorization']}

    base_url = PLAYLISTS_MS + '/playlists/songs'
    url = '/'.join((base_url, str(id)))

    r = requests.get(url, headers=headers)
    if r.status_code == 400:
        return RESP.response_400()
    if r.status_code == 404:
        return RESP.response_404(message='Playlist not found!')
    if r.status_code == 500:
        return RESP.response_500(message='Playlists_MS is down!')

    response_data = json.loads(r.text)

    song_ids = []
    for dictionary in response_data:
        song_ids.append(dictionary['song_id'])

    pool = multiprocessing.Pool(processes=len(song_ids))
    pool_outputs = pool.map(get_song, song_ids)
    pool.close()
    pool.join()

    return RESP.response_200(message=pool_outputs)


def get_song(id):
    """ Retrives a song given an id"""
    headers = {'Content-Type': 'application/json',
               'Authorization': request.headers['Authorization']}
    param = {'id': id}
    r = requests.get(SONGS_MS + '/songs', params=param, headers=headers)
    if r.status_code == 404:
        return RESP.response_404(message='Song not found!')
    if r.status_code == 500:
        return RESP.response_500(message='Songs_MS is down!')

    return json.loads(r.text)
