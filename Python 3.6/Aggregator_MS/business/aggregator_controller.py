import logging
import business.response_handling as RESP
import requests
import multiprocessing
import os
import json
from business.auth import requires_auth
from flask import request
from py_zipkin.zipkin import zipkin_span
from py_zipkin.zipkin import create_http_headers_for_new_span
from tracing.emp_zipkin_decorator import emp_zipkin_decorator


SONGS_MS = "http://" + os.environ['SONGSADDRESS']
PLAYLISTS_MS = "http://" + os.environ['PLAYLISTSADDRESS']


@emp_zipkin_decorator(service_name='aggregator_ms', span_name='aggregator_controller.hello_world', port=5004)
def hello_world():
    return RESP.response_200(message='Aggregator_MS working!')


@emp_zipkin_decorator(service_name='aggregator_ms', span_name='aggregator_controller.get_playlist_songs_info',
                      port=5004)
@requires_auth
def get_playlist_songs_info(id):
    """ Retrieves all playlist songs' information"""
    logging.debug("{aggregator_controller} BEGIN function get_playlist_songs_info()")

    if id is '':
        return RESP.response_400(message='A given parameter is empty')

    base_url = PLAYLISTS_MS + '/playlists/songs'
    url = '/'.join((base_url, str(id)))

    # Checks if song exists by sending a request into the Songs Microservice

    headers = {'Content-Type': 'application/json',
               'Authorization': request.headers['Authorization']}
    headers.update(create_http_headers_for_new_span())

    with zipkin_span(service_name='aggregator_ms', span_name='get_playlists_songs') as zipkin_context:
        r = requests.get(url, headers=headers)
        zipkin_context.update_binary_annotations({'http.method': 'GET', 'http.url': url,
                                                  'http.status_code': r.status_code})

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

    return RESP.response_200(message="Playlist Songs Info Retrieved Successfully")


@emp_zipkin_decorator(service_name='aggregator_ms', span_name='aggregator_controller.get_song', port=5004)
def get_song(id):
    """ Retrives a song given an id"""
    headers = {'Content-Type': 'application/json',
               'Authorization': request.headers['Authorization']}
    headers.update(create_http_headers_for_new_span())
    param = {'id': id}

    with zipkin_span(service_name='aggregator_ms', span_name='get_song') as zipkin_context:
        r = requests.get(SONGS_MS + '/songs', params=param, headers=headers)
        zipkin_context.update_binary_annotations({'http.method': 'GET', 'http.url': SONGS_MS + '/songs',
                                                  'http.status_code': r.status_code})

    if r.status_code == 404:
        return RESP.response_404(message='Song not found!')
    if r.status_code == 500:
        return RESP.response_500(message='Songs_MS is down!')

    return json.loads(r.text)
