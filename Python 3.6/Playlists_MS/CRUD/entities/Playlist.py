from CRUD.ORM import db
from datetime import datetime


class Playlist(db.Model):
    __tablename__ = 'playlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    size = db.Column(db.String(100), nullable=False, default=0)
    user_id = db.Column(db.Integer, nullable=False)

    def dump(self):
        return {'id': self.id, 'name': self.name, 'creation_date': self.creation_date, 'size': self.size, 'user_id': self.user_id}

    def __repr__(self):
        return "<Playlist('%s', '%s', '%s', %s)" % (self.name, self.creation_date, self.size, self.user_id)
