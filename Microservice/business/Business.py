from database import *
import hashlib
import logging
import connexion
from connexion.decorators.decorator import ResponseContainer
from flask import redirect, url_for, session
from flask_login import LoginManager, login_required, login_user, logout_user, current_user


# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


def get_user_songs(userID):
    logging.debug('{Business} BEGIN function get_user_songs()')
    songs = CRUD.read_user_songs(userID)
    # print 'OLAAA'
    # print userID
    # print 'DONE'
    logging.debug('{Business} END function get_user_songs()')
    logging.info('{Business} Songs retrieved')
    return [p.dump() for p in songs]



# starting connexion
app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app


# starting database
CRUD.create_tables()
CRUD.connect_database()


# config
application.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

# #flask-login
# login_manager = LoginManager()
# login_manager.init_app(application)
# login_manager.login_view = "login"
#
#
# # callback to reload the user object
# @login_manager.user_loader
# def load_user(userid):
#     return CRUD.read_user(id=userid)
#
#
# application.add_url_rule('/mySongs', view_func=post_song)
# application.add_url_rule('/myPlayLists', view_func=post_playlist)
# application.add_url_rule('/login', view_func=login)
# application.add_url_rule('/register', view_func=register)
# application.add_url_rule('/', view_func=home)



if __name__ == '__main__':
    app.run(port=5000)
