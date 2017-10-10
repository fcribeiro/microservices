from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy.orm import relationship

from Base import Base
import datetime


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, Sequence('playlist_id_seq'), primary_key=True)
    name = Column(String(90), nullable=False)
    creation_date = Column(String(90), nullable=False)  #CHANGE TO DATE
    size = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    songs = relationship("PlaylistSongs")

    def __init__(self, name, user_id):
        self.name = name
        self.creation_date = datetime.datetime.now()
        self.size = 0
        self.user_id = user_id

    def dump(self):
        return {'id': self.id, 'name': self.name, 'creation_date': self.creation_date, 'size': self.size}

    def __repr__(self):
        return "<Playlist('%s', '%s', '%s')" % (self.name, self.creation_date, self.size)


