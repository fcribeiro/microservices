import logging
import business.response_handling as RESP
import requests
import json
import jwt
import os
from py_zipkin.zipkin import zipkin_span
from py_zipkin.zipkin import create_http_headers_for_new_span
from business.emp_zipkin_decorator import emp_zipkin_decorator


USERS_MS = "http://" + os.environ['USERSADDRESS']
TOKEN_SECRET = 'secret'     # FIND WAY TO KEEP THIS SAFE!
ALGORITHM = 'HS256'


@emp_zipkin_decorator(service_name='authentication_ms', span_name='authentication_controller.hello_world', port=5003)
def hello_world():
    return RESP.response_200(message='Authentication_MS working!')


@emp_zipkin_decorator(service_name='authentication_ms', span_name='authentication_controller.create_token', port=5003)
def create_token(body):
    logging.debug("{authentication_controller} BEGIN function create_token()")

    if body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    payload = {'email': body['email'], 'password': body['password']}

    logging.debug("{authentication_controller} %s", USERS_MS)
    with zipkin_span(service_name='authentication_ms', span_name='create_token') as zipkin_context:
        headers = {}
        headers.update(create_http_headers_for_new_span())
        r = requests.post(USERS_MS + '/login', json=payload, headers=headers)
        zipkin_context.update_binary_annotations({'http.method': 'POST', 'http.url': USERS_MS + '/login',
                                                  'http.status_code': r.status_code})

    if r.status_code == requests.codes.ok:
        token_info = {
            'id': json.loads(r.content).get('id'),
            'name': json.loads(r.content).get('name'),
            'email': json.loads(r.content).get('email')
        }

        token = jwt.encode(token_info, TOKEN_SECRET, algorithm=ALGORITHM)
        return RESP.response_200(message={'token': token.decode('utf-8')})
    if r.status_code == 500:
        return RESP.response_500(message='Users_MS is down!')

    return RESP.response_400(message='Credentials are incorrect!')
