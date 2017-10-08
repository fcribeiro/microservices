import logging
import connexion
import requests
import json
# from flask_jwt import JWT, jwt_required, current_identity
# from werkzeug.security import safe_str_cmp

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def login():
    payload = {"username": "user1", "password": "abcxyz"}

    r = requests.post("http://localhost:5000/auth", data=json.dumps(payload), headers={'Content-Type': 'application/json'})
    return r.content


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app

# jwt = JWT(application, authenticate, identity)

# config
application.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)


if __name__ == '__main__':
    app.run(port=5004)
