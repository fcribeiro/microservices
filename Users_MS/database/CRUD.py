from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import logging
import hashlib
from Base import Base
from User import User

# Logging configuration
logging.basicConfig(datefmt='%d/%m/%Y %I:%M:%S', level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(message)s')

# database -> !!sensitive information!!
path = 'mysql+pymysql://root:ribeiro@localhost:3306/spotify'

session = None


def connect_database():
    logging.debug('{CRUD} BEGIN function connect_database()')
    engine = create_engine(path)
    logging.debug('{CRUD} Connect to database on path: %s', path)
    Session = sessionmaker(bind=engine)
    global session
    session = Session()
    logging.debug('{CRUD} END function connect_database()')
    logging.info('{CRUD} Connected to database')


# def connect_database():
#     logging.debug('{CRUD} BEGIN function connect_database()')
#     engine = create_engine(path)
#     logging.debug('{CRUD} Connect to database on path: %s', path)
#     Session = sessionmaker(bind=engine)
#     global session
#     session = Session()
#     logging.debug('{CRUD} Checking for admin..')
#     user = read_user(email='admin')
#     if user is None:
#         logging.debug('{CRUD} Admin not found!!')
#         sha = hashlib.sha1()
#         sha.update('admin')
#         create_user('admin', 'admin', sha.hexdigest())
#         logging.debug('{CRUD} Admin created')
#     logging.debug('{CRUD} END function connect_database()')
#     logging.info('{CRUD} Connected to database')


def create_tables():
    logging.debug('{CRUD} BEGIN function create_tables()')
    engine = create_engine(path)
    logging.debug('{CRUD} Connect to database on path: %s', path)
    Base.metadata.create_all(engine)
    logging.debug('{CRUD} END function create_tables()')
    logging.info('{CRUD} Tables created')


def read_user(email=None, id=None, password=None):
    logging.debug('{CRUD} BEGIN function read_user()')
    connect_database()
    query = None
    if password is not None:
        logging.debug('{CRUD} Searching for email: %s', email)
        query = session.query(User).filter_by(email=email)
        logging.debug('{CRUD} Found: %s', query.count())
        if query.count() != 0:
            user = query[0]
            logging.debug('{CRUD} Comparing passwords: %s vs %s', password, user.password)
            if password == user.password:
                logging.debug('{CRUD} END function read_user()')
                logging.info('{CRUD} User retrieved!!')
                return user
            logging.debug('{CRUD} Passwords dont match!!')
        logging.debug('{CRUD} END function read_user()')
        logging.info('{CRUD} No user found')
        return None
    if email is not None:
        logging.debug('{CRUD} Searching for email: %s', email)
        query = session.query(User).filter_by(email=email)
    if id is not None:
        logging.debug('{CRUD} Searching for id: %s', id)
        query = session.query(User).filter_by(id=id)
    logging.debug('{CRUD} Found: %s', query.count())
    if query.count() != 0:
        logging.debug('{CRUD} User found: %s', query[0])
        logging.debug('{CRUD} END function read_user()')
        logging.info('{CRUD} User retrieved')
        return query[0]
    logging.debug('{CRUD} END function read_user()')
    logging.info('{CRUD} No user found')
    return None


# CREATE
def create_user(name, email, password):
    logging.debug('{CRUD} BEGIN function create_user()')
    logging.debug('{CRUD} Name: %s', name)
    logging.debug('{CRUD} Email: %s', email)
    logging.debug('{CRUD} Password: %s', password)
    user = User(name, email, password)
    logging.debug('{CRUD} Creating user: %s', user)
    session.add(user)
    session.flush()
    session.commit()
    logging.debug('{CRUD} END function create_user()')
    logging.info('{CRUD} User created')


def update_user(user, name=None, email=None, password=None):
    logging.debug('{CRUD} BEGIN function update_user()')
    logging.debug('{CRUD} Before %s', user)
    if name is not None:
        logging.debug('{CRUD} Changing name: %s', name)
        user.name = name
    if email is not None:
        logging.debug('{CRUD} Changing email: %s', email)
        user.email = email
    if password is not None:
        logging.debug('{CRUD} Changing password: %s', password)
        user.password = password
    session.commit()
    logging.debug('{CRUD} After %s', user)
    logging.debug('{CRUD} END function update_user()')
    logging.info('{CRUD} User changed')
