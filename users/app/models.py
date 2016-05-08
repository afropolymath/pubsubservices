import datetime

from . import db
from werkzeug.security import generate_password_hash, \
     check_password_hash


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class User(db.Model, BaseModel):
    name = db.Column(db.String(100), nullable=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(100))

    def __init__(self, username, email, password, name=None):
        self.username = username
        self.email = email
        self.name = name
        self.set_password(password)

    def set_password(self, password):
        '''
        Set password to hashed version of <password> parameter
        '''
        self.password = generate_password_hash(password)

    def check_password(self, password):
        '''
        Check hashed password against <password> parameter>
        '''
        return check_password_hash(self.password, password)


def init():
    db.drop_all()
    db.create_all()
