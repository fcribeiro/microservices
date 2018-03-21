from CRUD.ORM import db
from CRUD.entities.Playlist import Playlist
from CRUD.entities.Playlist_Song import Playlist_Song


def create_database():
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    create_database()