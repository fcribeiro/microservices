from CRUD.ORM import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_deleted = db.Column(db.Boolean, default=False)

    def dump(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.email)
