from database import *
import logging
import connexion

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def post_user(name, email, password):
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


def get_user(email=None, user_id=None, password=None):
    logging.debug('{Business} BEGIN function get_user()')
    user = CRUD.read_user(email=email, id=user_id, password=password)
    logging.debug('{Business} END function get_user()')
    logging.info('{Business} User retrieved')
    return user.dump()


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


def put_user(user_id, name=None, email=None, password=None):
    logging.debug('{Business} BEGIN function put_user()')
    logging.debug('{Business} Parameters: %s, %s, %s', name, email, password)
    if name == "":
        name = None
    if email == "":
        email = None
    if password == "":
        password = None

    user = CRUD.read_user(id=user_id)
    CRUD.update_user(user, name, email, password)

    logging.debug('{Business} END function put_user()')
    logging.info('{Business} User updated')


# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app


# starting database
CRUD.create_tables()
CRUD.connect_database()


# config
application.config.update(
    DEBUG=True,
    SECRET_KEY='secret_xxx'
)


if __name__ == '__main__':
    app.run(port=5001)
