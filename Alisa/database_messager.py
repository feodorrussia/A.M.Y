from constants import *


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    status = db.Column(db.Integer)


class Settings(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id такой же как и у соответствующего пользователя
    bfp = db.Column(db.String(1000), unique=False, nullable=False)  # кнопки на главной странице(buttons on first page)
    ar_uid = db.Column(db.Integer)  # 1/0 автоматическое распознавание пользователя по id(automatic recognition of the user's id)*
    voice = db.Column(db.Integer)  # 1/0(будет ли Алиса озвучивать ответы)


class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(80), unique=False, nullable=False)
    friend = db.Column(db.String(80), unique=False, nullable=False)
    nickname = db.Column(db.String(80), unique=False, nullable=False)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    message = db.Column(db.String(1000), unique=False, nullable=False)
    recipient = db.Column(db.String(80), unique=False, nullable=False)
    status = db.Column(db.Integer)


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    users = db.Column(db.String(1000), unique=False, nullable=False)


db.create_all()
