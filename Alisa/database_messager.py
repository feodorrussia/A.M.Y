from constants import *


class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.Integer)


class Friend(db.Model):
    user = db.Column(db.String(80), unique=True, nullable=False)
    friend = db.Column(db.String(120), unique=False, nullable=False)


class Message(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False)
    message = db.Column(db.String(1000), unique=False, nullable=False)
    recipient = db.Column(db.String(80), unique=False, nullable=False)
    is_group_message = db.Column(db.Boolean)
    status = db.Column(db.Integer)


class Group(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    users = db.Column(db.String(1000), unique=False, nullable=False)


db.create_all()
