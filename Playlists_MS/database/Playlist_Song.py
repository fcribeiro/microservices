from sqlalchemy import Column, Integer, Sequence, ForeignKey
from Base import Base


class PlaylistSongs(Base):
    __tablename__ = 'playlist_songs'

    id = Column(Integer, Sequence('playlistSongs_id_seq'), primary_key=True)
    playlist_id = Column(Integer, ForeignKey('playlists.id'))
    song_id = Column(Integer, nullable=False)

    def __init__(self, playlist_id, song_id):
        self.playlist_id = playlist_id
        self.song_id = song_id

    def dump(self):
        return {'id': self.id, 'playlist_id': self.playlist_id, 'song_id': self.song_id}
