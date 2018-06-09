import logging
import os
import requests
import CRUD.CRUD_operations as CRUD
import business.response_handling as RESP
from flask import request
from business.auth import requires_auth
import socket

SONGS_MS = "http://" + os.environ['SONGSADDRESS']


def hello_world():
    return RESP.response_200(message='Playlists_MS working! -> Host: ' + socket.gethostname())


@requires_auth
def create_playlist(body):
    """ Creates a new playlist object given a name, and user id"""
    logging.debug("{users_controller} BEGIN function create_playlist()")

    if body['name'] is '' or body['user_id'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    try:
        playlist = CRUD.create_playlist(body['name'], body['user_id'])
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_500(message='Error adding playlist into database!')

    return RESP.response_201(message='Playlist created with success!')


@requires_auth
def update_playlist(id, body):
    """ Updates a playlist matching a given id with given the given name"""
    logging.debug("{users_controller} BEGIN function update_playlist()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    if body['name'] is '':
        return RESP.response_400(message='The name parameter is empty!')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    try:
        CRUD.update_playlist(playlist, name=body['name'])
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Playlist updated with success!')


@requires_auth
def get_playlist(id):
    """ Gets a playlist given an id"""
    logging.debug("{users_controller} BEGIN function get_playlist()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    return RESP.response_200(message=playlist.dump())


@requires_auth
def delete_playlist(id):
    """ Deletes a playlist"""
    logging.debug("{users_controller} BEGIN function delete_playlist()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    try:
        CRUD.delete_object(playlist)

        entries = CRUD.read_songs_from_playlist(id)

        for entry in entries:
            CRUD.delete_object(entry)

        CRUD.commit()
    except Exception:
        CRUD.rollback()
        RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Playlist deleted with success')


@requires_auth
def get_user_playlists(user_id):
    """ Retrieves all user playlists"""
    logging.debug("{users_controller} BEGIN function get_user_playlists()")

    if user_id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        playlists = CRUD.read_all_user_playlists(user_id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    array = []

    for playlist in playlists:
        array.append(playlist.dump())

    return RESP.response_200(message=array)


@requires_auth
def add_song_to_playlist(id, song_id, user_id):
    """ Adds a song into a playlist"""
    logging.debug("{users_controller} BEGIN function add_song_to_playlist()")

    if id is '' or song_id is '' or user_id is '':
        return RESP.response_400(message='A given parameter is empty')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    if playlist.user_id != user_id:
        return RESP.response_400(message='This playlist belongs to another user')

    # Checks if song exists by sending a request into the Songs Microservice
    headers = {'Content-Type': 'application/json',
               'Authorization': request.headers['Authorization']}
    param = {'id': song_id}
    r = requests.get(SONGS_MS + '/songs', params=param, headers=headers)
    if r.status_code == 404:
        return RESP.response_404(message='Song not found!')
    if r.status_code == 500:
        return RESP.response_500(message='Songs_MS is down!')

    try:
        CRUD.create_song_in_playlist(id, song_id)
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Song added into playlist with success!')


@requires_auth
def delete_song_from_playlist(id, song_id, user_id):
    """ Removes a song from a playlist"""
    logging.debug("{users_controller} BEGIN function delete_song_from_playlist()")

    if id is '' or song_id is '' or user_id is '':
        return RESP.response_400(message='A given parameter is empty')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    if playlist.user_id != user_id:
        return RESP.response_400(message='This playlist belongs to another user')

    try:
        playlist_song = CRUD.read_song_from_playlist(id, song_id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist_song is None:
        return RESP.response_404(message='Song not found is playlist')

    try:
        CRUD.delete_object(playlist_song)
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Song removed from playlist with success')


@requires_auth
def get_playlist_songs(id):
    """ Retrieves all playlist songs' ids"""
    logging.debug("{users_controller} BEGIN function delete_song_from_playlist()")

    if id is '':
        return RESP.response_400(message='A given parameter is empty')

    try:
        playlist = CRUD.read_playlist_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    try:
        songs = CRUD.read_songs_from_playlist(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    array = []

    for song in songs:
        array.append(song.dump())

    return RESP.response_200(message=array)
