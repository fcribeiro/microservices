import logging
import business.response_handling as RESP
import requests
import json
import jwt
import os

# USERS_MS = 'http://0.0.0.0:5000'
USERS_MS = "http://" + os.environ['USERSADDRESS']
TOKEN_SECRET = 'secret'     # FIND WAY TO KEEP THIS SAFE!
ALGORITHM = 'HS256'


def hello_world():
    return RESP.response_200(message='Authentication_MS working!')


def create_token(body):
    logging.debug("{authentication_controller} BEGIN function create_token()")

    if body['email'] is '' or body['password'] is '':
        return RESP.response_400(message='A given parameter is empty!')

    payload = {'email': body['email'], 'password': body['password']}

    r = requests.post(USERS_MS + '/login', json=payload)
    if r.status_code == requests.codes.ok:
        token_info = {
            'id': json.loads(r.content).get('id'),
            'name': json.loads(r.content).get('name'),
            'email': json.loads(r.content).get('email')
        }

        token = jwt.encode(token_info, TOKEN_SECRET, algorithm=ALGORITHM)
        return RESP.response_200(message={'token': token.decode('utf-8')})

    return RESP.response_400(message='Credentials are incorrect!')
