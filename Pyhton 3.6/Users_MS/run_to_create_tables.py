from CRUD.ORM import db
from CRUD.entities.User import User


def create_database():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    create_database()