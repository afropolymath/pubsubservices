import datetime
import sqlite3

from sqlalchemy.engine import Engine
from sqlalchemy import event

from . import db


class BaseModel(object):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class Publication(db.Model, BaseModel):
    title = db.Column(db.String(100))
    description = db.Column(db.String(200))
    creator_id = db.Column(db.Integer)


class Subscription(db.Model, BaseModel):
    user_id = db.Column(db.Integer)
    publication_id = db.Column(db.Integer, db.ForeignKey(Publication.id))
    publication = db.relationship(
        'Publication',
        backref=db.backref(
            'subscriptions',
            lazy="dynamic"
        )
    )


def init():
    db.drop_all()
    db.create_all()


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    if type(dbapi_connection) is sqlite3.Connection:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
