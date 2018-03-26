import connexion as connexion
from business.playlists_controller import *
from CRUD.ORM import db, create_database


# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')


app = connexion.App(__name__)
app.add_api('swagger.yaml')
application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db.session.remove()


if __name__ == '__main__':
    create_database()
    app.run(port=5002, debug=True)
