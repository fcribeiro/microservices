import logging

from py_zipkin.stack import ThreadLocalStack

import CRUD.CRUD_operations as CRUD
import business.response_handling as RESP
import business.utils as UTILS
from business.auth import requires_auth
from flask import request
from business.emp_zipkin_decorator import emp_zipkin_decorator
from py_zipkin.zipkin import zipkin_span, ZipkinAttrs


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.hello_world', port=5000)
def hello_world():
    return RESP.response_200(message='Users_MS working!')


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.create_user', port=5000)
def create_user(body):
    """ Creates a new user object given a name, email and password"""
    logging.debug("{users_controller} BEGIN function create_user()")

    if body['name'] is '' or body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    try:
        if CRUD.read_user_by_email(body['email']) is not None:
            return RESP.response_409(message='The given email is already in use!')
    except Exception:
        return RESP.response_500(message='Database is down!')

    try:
        user = CRUD.create_user(body['name'], body['email'], UTILS.hash_password(body['password']))
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    if user is None:
        return RESP.response_500(message='Error adding user into database!')

    return RESP.response_201(message='User created with success!')


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.read_user', port=5000)
@requires_auth
def read_user(email):
    """ Returns an active user (if any) given an email"""
    logging.debug("{users_controller} BEGIN function read_user()")

    if email is '':
        return RESP.response_400(message='The email parameter is empty!')

    try:
        user = CRUD.read_user_by_email_not_deleted(email)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if user is None:
        return RESP.response_404(message='User not found!')

    return RESP.response_200(message=user.dump())


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.update_user', port=5000)
@requires_auth
def update_user(id, body):
    """ Updates an active user matching a given id with given parameters such as name, email and password. When a
    parameter is empty it is not updated"""
    logging.debug("{users_controller} BEGIN function update_user()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        user = CRUD.read_user_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if user is None:
        return RESP.response_404(message='User not found!')

    try:
        if body['email'] is not '' and body['email'] != user.email:
            user_email = CRUD.read_user_by_email(body['email'])
            if user_email is not None:
                return RESP.response_409(message='The given email is already in use!')
    except Exception:
        return RESP.response_500(message='Database is down!')

    try:
        CRUD.update_user(user, body['name'], body['email'], UTILS.hash_password(body['password']))
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='User updated with success!')


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.delete_user', port=5000)
@requires_auth
def delete_user(id):
    """ Deletes an active user given an id"""
    logging.debug("{users_controller} BEGIN function delete_user()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    try:
        user = CRUD.read_user_by_id(id)
    except Exception:
        return RESP.response_500(message='Database is down!')

    if user is None:
        return RESP.response_404(message='User not found!')

    try:
        CRUD.delete_user(user)
        CRUD.commit()
    except Exception:
        CRUD.rollback()
        return RESP.response_500(message='Database is down!')

    return RESP.response_200(message='User deleted with success')


@emp_zipkin_decorator(service_name='users_ms', span_name='users_controller.check_login', port=5000)
def check_login(body):
    """ Checks the login parameters"""
    logging.debug("{users_controller} BEGIN function check_login()")

    if body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    user = CRUD.read_user_by_email_not_deleted(body['email'])
    try:
        user = CRUD.read_user_by_email_not_deleted(body['email'])
    except Exception:
        return RESP.response_500(message='Database is down!')

    if user is None:
        return RESP.response_400(message='Bad login!')

    if UTILS.hash_password(body['password']) != user.password:
        return RESP.response_400(message='Bad login!')

    return RESP.response_200(message=user.dump())


