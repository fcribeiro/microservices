import logging
import CRUD.CRUD_operations as CRUD
import business.response_handling as RESP
from business.auth import requires_auth


def hello_world():
    return RESP.response_200(message='Playlists_MS working!')


@requires_auth
def create_playlist(body):
    """ Creates a new playlist object given a name, and user id"""
    logging.debug("{users_controller} BEGIN function create_playlist()")

    if body['name'] is '' or body['user_id'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    playlist = CRUD.create_playlist(body['name'], body['user_id'])
    CRUD.commit()

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

    playlist = CRUD.read_playlist_by_id(id)

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    CRUD.update_playlist(playlist, name=body['name'])
    CRUD.commit()

    return RESP.response_200(message='Playlist updated with success!')


@requires_auth
def get_playlist(id):
    """ Gets a playlist given an id"""
    logging.debug("{users_controller} BEGIN function get_playlist()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    playlist = CRUD.read_playlist_by_id(id)

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    return RESP.response_200(message=playlist.dump())


@requires_auth
def delete_playlist(id):
    """ Deletes a playlist"""
    logging.debug("{users_controller} BEGIN function delete_playlist()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    playlist = CRUD.read_playlist_by_id(id)

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
        RESP.response_500(message='An error has occurred')

    return RESP.response_200(message='Playlist deleted with success')


@requires_auth
def get_user_playlists(user_id):
    """ Retrieves all user playlists"""
    logging.debug("{users_controller} BEGIN function get_user_playlists()")

    if user_id is '':
        return RESP.response_400(message='The id parameter is empty!')

    playlists = CRUD.read_all_user_playlists(user_id)

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

    playlist = CRUD.read_playlist_by_id(id)

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    if playlist.user_id != user_id:
        return RESP.response_400(message='This playlist belongs to another user')

    # TODO: Check if song exists by sending a request into the Songs Microservice

    CRUD.create_song_in_playlist(id, song_id)
    CRUD.commit()

    return RESP.response_200(message='Song added into playlist with success!')


@requires_auth
def delete_song_from_playlist(id, song_id, user_id):
    """ Removes a song from a playlist"""
    logging.debug("{users_controller} BEGIN function delete_song_from_playlist()")

    if id is '' or song_id is '' or user_id is '':
        return RESP.response_400(message='A given parameter is empty')

    playlist = CRUD.read_playlist_by_id(id)

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    if playlist.user_id != user_id:
        return RESP.response_400(message='This playlist belongs to another user')

    playlist_song = CRUD.read_song_from_playlist(id, song_id)

    if playlist_song is None:
        return RESP.response_404(message='Song not found is playlist')

    CRUD.delete_object(playlist_song)
    CRUD.commit()

    return RESP.response_200(message='Song removed from playlist with success')


@requires_auth
def get_playlist_songs(id):
    """ Retrieves all playlist songs' ids"""
    logging.debug("{users_controller} BEGIN function delete_song_from_playlist()")

    if id is '':
        return RESP.response_400(message='A given parameter is empty')

    playlist = CRUD.read_playlist_by_id(id)

    if playlist is None:
        return RESP.response_404(message='Playlist not found!')

    songs = CRUD.read_songs_from_playlist(id)

    array = []

    for song in songs:
        array.append(song.dump())

    return RESP.response_200(message=array)
