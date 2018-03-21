import logging
import CRUD.CRUD_operations as CRUD
import business.response_handling as RESP
import business.utils as UTILS
from business.auth import requires_auth


def hello_world():
    return RESP.response_200(message='Users_MS working!')


def create_user(body):
    """ Creates a new user object given a name, email and password"""
    logging.debug("{users_controller} BEGIN function create_user()")

    if body['name'] is '' or body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    if CRUD.read_user_by_email(body['email']) is not None:
        return RESP.response_409(message='The given email is already in use!')

    user = CRUD.create_user(body['name'], body['email'], UTILS.hash_password(body['password']))
    CRUD.commit()

    if user is None:
        return RESP.response_500(message='Error adding user into database!')

    return RESP.response_201(message='User created with success!')


@requires_auth
def read_user(email):
    """ Returns an active user (if any) given an email"""
    logging.debug("{users_controller} BEGIN function read_user()")

    if email is '':
        return RESP.response_400(message='The email parameter is empty!')

    user = CRUD.read_user_by_email_not_deleted(email)

    if user is None:
        return RESP.response_404(message='User not found!')

    return RESP.response_200(message=user.dump())


@requires_auth
def update_user(id, body):
    """ Updates an active user matching a given id with given parameters such as name, email and password. When a
    parameter is empty it is not updated"""
    logging.debug("{users_controller} BEGIN function update_user()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    user = CRUD.read_user_by_id(id)

    if user is None:
        return RESP.response_404(message='User not found!')

    if body['email'] is not '' and body['email'] != user.email:
        user_email = CRUD.read_user_by_email(body['email'])
        if user_email is not None:
            return RESP.response_409(message='The given email is already in use!')

    CRUD.update_user(user, body['name'], body['email'], UTILS.hash_password(body['password']))
    CRUD.commit()

    return RESP.response_200(message='User updated with success!')


@requires_auth
def delete_user(id):
    """ Deletes an active user given an id"""
    logging.debug("{users_controller} BEGIN function delete_user()")

    if id is '':
        return RESP.response_400(message='The id parameter is empty!')

    user = CRUD.read_user_by_id(id)

    if user is None:
        return RESP.response_404(message='User not found!')

    CRUD.delete_user(user)
    CRUD.commit()

    return RESP.response_200(message='User deleted with success')


def check_login(body):
    """ Checks the login parameters"""
    logging.debug("{users_controller} BEGIN function delete_user()")

    if body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    user = CRUD.read_user_by_email_not_deleted(body['email'])

    if user is None:
        return RESP.response_400(message='Bad login!')

    if UTILS.hash_password(body['password']) != user.password:
        return RESP.response_400(message='Bad login!')

    return RESP.response_200(message=user.dump())


