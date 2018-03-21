from sqlalchemy import Column, Integer, String, Sequence, Boolean

from Base import Base


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, Sequence('song_id_seq'), primary_key=True)
    title = Column(String(90), nullable=False)
    artist = Column(String(90), nullable=False)
    album = Column(String(90), nullable=False)
    release_year = Column(Integer, nullable=False)
    path = Column(String(90), nullable=False)
    user_id = Column(Integer, nullable=False)
    is_deleted = Column(Boolean)

    def __init__(self, title, artist, album, release_year, path, userID):
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.path = path
        self.user_id = userID
        self.is_deleted = False

    def dump(self):
        return {'id': self.id, 'title': self.title, 'artist': self.artist, 'album': self.album, 'release_year': self.release_year, 'user_id': self.user_id}

    def __repr__(self):
        return "<Song('%s', '%s', '%s', '%s', '%s')>" % (self.title, self.artist, self.album, self.release_year, self.path)
