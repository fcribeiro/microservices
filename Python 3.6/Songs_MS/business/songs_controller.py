import logging
import CRUD.CRUD_operations as CRUD
import business.response_handling as RESP
from business.auth import requires_auth
import time
import random
from py_zipkin.zipkin import zipkin_span
from tracing.emp_zipkin_decorator import emp_zipkin_decorator
from py_zipkin.stack import ThreadLocalStack


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.hello_world', port=5001,
                      binary_annotations={'foo': 'bar', 'test1': 'test2'})
def hello_world():
    z_attrs = ThreadLocalStack().get()
    print(z_attrs)
    with zipkin_span(service_name='songs_ms', span_name='before_hey_test') as zipkin_context:
        hey_test(5)
        zipkin_context.update_binary_annotations({'result': "YEEEEEE"})
    return RESP.response_200(message='Songs_MS working!')


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.hey_test', port=5001,
                      binary_annotations={'foo': 'bar'})
def hey_test(id):
    print("HEYYYYYYYYYYY")
    return RESP.response_200(message='Songs_MS working!')


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.create_song', port=5001)
@requires_auth
def create_song(body):
    logging.debug("{songs_controller} BEGIN function create_song()")

    if body['title'] is '' or body['artist'] is '' or body['album'] is '' or body['release_year'] is '' or body[
        'path'] is '' or body['user_id'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    try:
        song = CRUD.create_song(body['title'], body['artist'], body['album'], body['release_year'], body['path'],
                                body['user_id'])
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    if song is None:
        return RESP.response_500(message='Error adding song into database!')

    time.sleep(random.expovariate(3))
    return RESP.response_201(message='Song created with success!')


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.read_song', port=5001)
@requires_auth
def read_song(id):
    """ Returns a song (if any) given an id"""
    logging.debug("{songs_controller} BEGIN function read_song()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        song = CRUD.read_song_by_song_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if song is None:
        return RESP.response_404(message='Song not found!')

    return RESP.response_200(message=song.dump())


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.read_songs_criteria', port=5001)
@requires_auth
def read_songs_criteria(expression):
    """ Returns a list of songs given an expression"""
    logging.debug("{songs_controller} BEGIN function read_song_criteria()")

    try:
        songs = CRUD.read_songs_by_criteria(expression)
    except Exception:
        return RESP.response_500(message='Database is down!')

    array = []

    for song in songs:
        array.append(song.dump())

    return RESP.response_200(message=array)


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.update_song', port=5001)
@requires_auth
def update_song(id, body):
    """ Updates an active song matching a given id with given parameters such as title, artist, album, release year and
    path. When a parameter is empty it is not updated"""
    logging.debug("{songs_controller} BEGIN function update_song()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        song = CRUD.read_song_by_song_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if song is None:
        return RESP.response_404(message='Song not found!')

    try:
        CRUD.update_song(song, body['title'], body['artist'], body['album'], body['release_year'], body['path'])
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Song updated with success!')


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.delete_song', port=5001)
@requires_auth
def delete_song(id):
    """ Deletes an active song given an id"""
    logging.debug("{songs_controller} BEGIN function delete_song()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        song = CRUD.read_song_by_song_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if song is None:
        return RESP.response_404(message='Song not found!')

    try:
        CRUD.delete_song(song)
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='Song deleted with success')


@emp_zipkin_decorator(service_name='songs_ms', span_name='songs_controller.convert_song', port=5001)
@requires_auth
def convert_song(id):
    """ Converts a song from .mp3 to .wav"""
    logging.debug("{songs_controller} BEGIN function convert_song()")

    time.sleep(random.expovariate(3 / 2))

    return RESP.response_200(message='Song converted with success')
