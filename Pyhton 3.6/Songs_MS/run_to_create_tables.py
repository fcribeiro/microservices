from CRUD.ORM import db
from CRUD.entities.Song import Song


def create_database():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    create_database()