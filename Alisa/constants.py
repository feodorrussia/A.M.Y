from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sqldatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = SQLAlchemy(app)

bfp_i = ['Друзья', 'Помощь', 'Настройки', 'Выйти']  # кнопки на главной странице(buttons on first page)
bop = ['Помощь', 'Войти']  # кнопки на начальной странице(buttons on out page)
btc = ['Друзья', 'Помощь', 'Найти друга', 'Написать другу', 'Настройки', 'Выйти']  # все кнопки
bfc = ['Написать сообщение', 'Найти', 'Главная']
bfse = ['Найти', 'Главная']
ib = ['Помощь', 'Главная']
cb = ['Обновить', 'Распечатать историю диалога', 'Друзья', 'Помощь', 'Главная']
bc = ['Друзья', 'Помощь', 'Настройки', 'Главная']


hwc = ['помощь']
ewc = ['выйти', 'выйди']
afwc = ['друзья', 'вернись в друзья']
gfpwc = ['главная', 'отбой, давай на главную']
swc = ['найти', 'найди']
osc = ['login', 'out']
ywc = ['да']
nwc = ['нет']
uwc = ['обновить']
stwc = ['настройки']
