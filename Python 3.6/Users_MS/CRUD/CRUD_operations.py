import logging
from CRUD.ORM import db
from CRUD.entities.User import User
from business.emp_zipkin_decorator import emp_zipkin_decorator

# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- BASE STUFF ----------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.commit', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def commit():
    logging.debug("{CRUD_operations} BEGIN function commit()")
    db.session.commit()
    logging.info("{CRUD_operations} Performed COMMIT to the database")


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.rollback', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def rollback():
    logging.debug("{CRUD_operations} BEGIN function rollback()")
    db.session.rollback()
    logging.info("{CRUD_operations} Performed ROLLBACK to the database")


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- CREATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.create_user', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def create_user(name, email, password):
    logging.debug('{CRUD_operations} BEGIN function create_user()')
    logging.debug('{CRUD_operations} Data received: name: %s, email: %s, password: %s', name, email, password)
    user = User(name=name, email=email, password=password)
    db.session.add(user)
    logging.debug('{CRUD_operations} END function create_user()')
    return user


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- READ ----------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.read_user_by_email', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def read_user_by_email(email):
    """ Checks for all users given an email"""
    logging.debug('{CRUD_operations} BEGIN function read_user_by_email()')
    logging.debug('{CRUD_operations} Data received: email: %s', email)
    user = User.query.filter_by(email=email).first()
    logging.debug('{CRUD_operations} END function read_user_by_email()')
    return user


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.read_user_by_email', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def read_user_by_email_not_deleted(email):
    """ Checks for all users given an email"""
    logging.debug('{CRUD_operations} BEGIN function read_user_by_email_not_deleted()')
    logging.debug('{CRUD_operations} Data received: email: %s', email)
    user = User.query.filter_by(email=email).filter_by(is_deleted=False).first()
    logging.debug('{CRUD_operations} END function read_user_by_email_not_deleted()')
    return user


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.read_user_by_id', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def read_user_by_id(id):
    """ Checks for users that are not deleted given an id"""
    logging.debug('{CRUD_operations} BEGIN function read_user_by_id()')
    logging.debug('{CRUD_operations} Data received: id: %s', id)
    user = User.query.filter_by(id=id).filter_by(is_deleted=False).first()
    logging.debug('{CRUD_operations} END function read_user_by_id()')
    return user


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- UPDATE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.update_user', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def update_user(user, name, email, password):
    logging.debug('{CRUD_operations} BEGIN function update_user()')
    logging.debug('{CRUD_operations} Data received: user: %s', user)
    if name is not '':
        user.name = name
    if email is not '':
        user.email = email
    if password is not '':
        user.password = password
    logging.debug('{CRUD_operations} END function update_user()')
    return user


# ---------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- DELETE --------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------------


@emp_zipkin_decorator(service_name='users_ms', span_name='CRUD_operations.delete_user', port=5000,
                      binary_annotations={'db.instance': 'Users_MS', 'db.type': 'sqlalchemy'})
def delete_user(user):
    """ Fake deletes an user. Just change a variable is_deleted to True"""
    logging.debug('{CRUD_operations} BEGIN function delete_user()')
    logging.debug('{CRUD_operations} Data received: user: %s', user)
    user.is_deleted = True
    logging.debug('{CRUD_operations} END function delete_user()')
