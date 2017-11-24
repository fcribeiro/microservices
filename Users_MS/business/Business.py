from database import *
import logging
import connexion
from flask_jwt import JWT, jwt_required, current_identity, request
from werkzeug.security import safe_str_cmp
from sqlalchemy import exc
import time

from py_zipkin.zipkin import zipkin_span, create_http_headers_for_new_span, ZipkinAttrs

import requests
import time

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def http_transport(encoded_span):
    # The collector expects a thrift-encoded list of spans. Instead of
    # decoding and re-encoding the already thrift-encoded message, we can just
    # add header bytes that specify that what follows is a list of length 1.
    body = '\x0c\x00\x00\x00\x01' + encoded_span
    logging.info('{ZIPKIN} transporting')
    requests.post(
        'http://zipkin:9411/api/v1/spans',
        data=body,
        headers={'Content-Type': 'application/x-thrift'},
    )


def post_user(name, email, password):
    with zipkin_span(
        service_name='users_ms',
        zipkin_attrs=ZipkinAttrs(
            trace_id=request.headers['X-B3-TraceID'],
            span_id=request.headers['X-B3-SpanID'],
            parent_span_id=request.headers['X-B3-ParentSpanID'],
            flags=request.headers['X-B3-Flags'],
            is_sampled=request.headers['X-B3-Sampled'],
        ),
        span_name='post_user',
        transport_handler=http_transport,
        port=5000,
        sample_rate=100,
    ):
        logging.debug('{Business} BEGIN function post_user()')
        logging.debug('{Business} Parameters: %s, %s, %s', name, email, password)
        if user_exists(email):
            logging.debug('{Business} END function post_user()')
            logging.info('{Business} Cant add user!!')
            return {'response': 'True'}
        CRUD.create_user(name, email, password)
        logging.debug('{Business} END function post_user()')
        logging.info('{Business} User added')
    return {'response': 'False'}


@jwt_required()
def get_user(email=None, password=None):
    logging.debug('{Business} BEGIN function get_user()')
    user = CRUD.read_user(email=email, id=current_identity.get_id(), password=password)
    logging.debug('{Business} END function get_user()')
    logging.info('{Business} User retrieved')
    return user.dump()


@jwt_required()
def get_admin():
    logging.debug('{Business} BEGIN function get_admin()')
    user = CRUD.read_user(email='admin')
    logging.debug('{Business} END function get_admin()')
    logging.info('{Business} User retrieved')
    return user.dump()['id']


def user_exists(email):
    logging.debug('{Business} BEGIN function user_exists()')
    logging.debug('{Business} Checking email: %s', email)
    user = CRUD.read_user(email=email)
    logging.debug('{Business} END function user_exists()')
    if user is None:
        logging.info('{Business} No users found with the same email!!')
        return False
    logging.info('{Business} Email already in use!!')
    return True


@jwt_required()
def put_user(name=None, email=None, password=None):
    logging.debug('{Business} BEGIN function put_user()')
    logging.debug('{Business} Parameters: %s, %s, %s', name, email, password)
    if name == "":
        name = None
    if email == "":
        email = None
    if password == "":
        password = None

    user = CRUD.read_user(id=current_identity.get_id())
    CRUD.update_user(user, name, email, password)
    logging.debug('{Business} END function put_user()')
    logging.info('{Business} User updated')


@jwt_required()
def del_user():
    logging.debug('{Business} BEGIN function del_user()')
    logging.debug('{Business} Deleting User: %s', current_identity)
    CRUD.delete_something(current_identity)
    logging.debug('{Business} END function del_user()')


def authenticate(username, password):
    logging.debug('{Business} BEGIN function authenticate()')
    user = CRUD.read_user(email=username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        logging.debug('{Business} END function authenticate()')
        return user


def identity(payload):
    user_id = payload['identity']
    user = CRUD.read_user(id=user_id)
    return user


@jwt_required()
def protected():

    # print current_identity.get_id()
    return '%s' % current_identity


# starting connexion
app = connexion.App(__name__)

app.add_api('swagger.yaml')
application = app.app

application.config['SECRET_KEY'] = 'super-secret'
app.debug = True




jwt = JWT(application, authenticate, identity)

# starting database
while True:
    try:
        CRUD.create_tables()
        CRUD.connect_database()
    except exc.SQLAlchemyError:
        print 'DATABASE Exception'
        time.sleep(3)
        continue
    break


if __name__ == '__main__':
    app.run(port=5000)
