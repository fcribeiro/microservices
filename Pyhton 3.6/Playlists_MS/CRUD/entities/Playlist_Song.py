from CRUD.ORM import db


class Playlist_Song(db.Model):
    __tablename__ = 'playlist_songs'
    id = db.Column(db.Integer, primary_key=True)
    playlist_id = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, nullable=False)

    def dump(self):
        return {'song_id': self.song_id}

    def __repr__(self):
        return "<Playlist_Song('%s', '%s')" % (self.playlist_id, self.song_id)