from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from Base import Base
from User import User
from Playlist_Song import playlist_song


class Song(Base):
    __tablename__ = 'songs'

    id = Column(Integer, Sequence('song_id_seq'), primary_key=True)
    title = Column(String(90), nullable=False)
    artist = Column(String(90), nullable=False)
    album = Column(String(90), nullable=False)
    release_year = Column(Integer, nullable=False)
    path = Column(String(90), nullable=False)
    is_deleted = Column(Boolean)

    # one to many association User<->Song
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="songs")

    # many to many association Playlist<->Song
    playlists = relationship("Playlist", secondary=playlist_song, back_populates="songs")

    def __init__(self, title, artist, album, release_year, path):
        self.title = title
        self.artist = artist
        self.album = album
        self.release_year = release_year
        self.path = path
        self.is_deleted = False

    def dump(self):
        return {'id': self.id, 'title': self.title, 'artist': self.artist, 'album': self.album, 'release_year': self.release_year}

    def __repr__(self):
        return "<Song('%s', '%s', '%s', '%s', '%s') - User->'%s'>" % (self.title, self.artist, self.album, self.release_year, self.path, self.user.name)


User.songs = relationship("Song", order_by=Song.id, back_populates="user")
