from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import relationship
from User import User
from Base import Base
from Playlist_Song import playlist_song
import datetime


class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(Integer, Sequence('playlist_id_seq'), primary_key=True)
    name = Column(String(90), nullable=False)
    creation_date = Column(String(90), nullable=False)  #CHANGE TO DATE
    size = Column(Integer, nullable=False)

    # one to many association User<->Playlist
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="playlists")

    # many to many association Playlist<->Song
    songs = relationship("Song", secondary=playlist_song, back_populates="playlists")

    def __init__(self, name):
        self.name = name
        self.creation_date = datetime.datetime.now()
        self.size = 0

    def dump(self):
        return {'id': self.id, 'name': self.name, 'creation_date': self.creation_date, 'size': self.size}

    def __repr__(self):
        return "<Playlist('%s', '%s', '%s') - User->'%s'>" % (self.name, self.creation_date, self.size, self.user.name)


User.playlists = relationship("Playlist", order_by=Playlist.id, back_populates="user")

