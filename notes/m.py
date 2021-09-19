from datetime import datetime
from flask_login import UserMixin
from notes.e import db


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tittle = db.Column(db.String(20))
    body = db.Column(db.Text())
    time_stamp = db.Column(db.DateTime, default=datetime.utcnow)
    uuid = db.Column(db.String(129))
    u_id = db.Column(db.Integer, db.ForeignKey('users.id'))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    password = db.Column(db.Text())
    notes = db.relationship('Notes')


@db.event.listens_for(Notes.body, 'set', named=True)
def time_stamp_change(**kwargs):
    if kwargs['target'].time_stamp is not None:
        kwargs['target'].time_stamp = datetime.utcnow()
