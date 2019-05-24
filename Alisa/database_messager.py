from constants import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.Integer)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=True, nullable=False)
    friend = db.Column(db.String(80), unique=False, nullable=False)
    nicname = db.Column(db.String(80), unique=False, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    message = db.Column(db.String(1000), unique=False, nullable=False)
    recipient = db.Column(db.String(80), unique=False, nullable=False)
    is_group_message = db.Column(db.Boolean)
    status = db.Column(db.Integer)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.Column(db.String(1000), unique=False, nullable=False)


db.create_all()
