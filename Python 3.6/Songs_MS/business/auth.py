import logging
from functools import wraps
from flask import request
import business.response_handling as RESP
import jwt

TOKEN_SECRET = 'secret'     # FIND WAY TO KEEP THIS SAFE!
ALGORITHM = 'HS256'


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        logging.debug("{auth} BEGIN function requires_auth()")
        try:
            token = request.headers['Authorization']
        except Exception:
            return RESP.response_401()

        try:
            check_token(token)
        except jwt.InvalidTokenError:
            return RESP.response_401()

        return f(*args, **kwargs)

    return decorated


def check_token(token):
    logging.debug("{auth} BEGIN function check_token()")

    options = {
        'verify_signature': True,
        'verify_exp': True,
        'verify_nbf': True,
        'verify_iat': True,
        'verify_aud': True,
        'require_exp': False,
        'require_iat': False,
        'require_nbf': False
    }

    payload = jwt.decode(token, TOKEN_SECRET, algorithms=[ALGORITHM], options=options)

    return payload
