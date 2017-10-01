from sqlalchemy import Column, Integer, String, Sequence
from Base import Base
from flask_login import UserMixin


class User(Base, UserMixin):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id_seq'), primary_key=True)
    name = Column(String(90), nullable=False)
    email = Column(String(90), nullable=False)
    password = Column(String(90), nullable=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def dump(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.name, self.email, self.password)





