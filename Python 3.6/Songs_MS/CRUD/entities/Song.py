from CRUD.ORM import db


class Song(db.Model):
    __tablename__ = 'songs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    album = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=False)
    path = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def dump(self):
        return {'title': self.title, 'artist': self.artist, 'album': self.album, 'release_year': self.release_year, 'path': self.path, 'user_id': self.user_id}

    def __repr__(self):
        return "<Song('%s', '%s', '%s', '%s', '%s')>" % (self.title, self.artist, self.album, self.release_year, self.path)
