from flask import Flask
from flask_sqlalchemy import SQLAlchemy


# app is the object for flask managent
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_pyfile('../config.cfg')
# db is now our orm manager
db = SQLAlchemy(app)


