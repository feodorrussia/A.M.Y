# coding: utf-8
from __future__ import unicode_literals
from little_fuctions import *
from database_messager import *


def handle_dialog(request, response, user_storage, database):
    if not user_storage:
        user_storage = {"suggests": ['Помощь']}
    input_message = request.command.lower()

    if request.user_id not in database.get_session(all=True):
        database.add_session(request.user_id)
        print(database.get_session(request.user_id))

    if input_message in ['выйти', 'выйди']:
        user_storage = {"suggests": ['Помощь', 'Войти']}
        user_name = database.get_session(request.user_id, 'user_name')
        user = User.query.filter_by(username=user_name).first()
        user.status = 0
        db.session.commit()
        database.update(request.user_id, 'login')
        return message_return(response, user_storage,
                              'Пока! До новых встреч;)')

    if database.get_session(request.user_id, 'status_action')[0] == 'login' and len(
            input_message.split()) == 2:
        user_name, password = request.command.split()
        if User.query.filter_by(username=user_name).all():  # Проверка на нового пользователя
            user = User.query.filter_by(username=user_name).first()
            if user.password == password:  # Проверка на правильность пароля
                user_storage = {'suggests': ['Друзья', 'Помощь', 'Настройки', 'Выйти']}
                database.update(request.user_id, user_name, 'user_name')
                database.update(request.user_id, 'first')
                return message_return(response, user_storage, 'Добро пожаловать!' + new_message())
            else:  # Информирование об ошибке
                return message_return(response, user_storage,
                                      'Ошибка!) Попробуй ещё раз, но помни, логин должен быть индивидуальным!')
        else:  # Создание нового пользователя
            user_storage = {'suggests': ['Друзья', 'Помощь', 'Настройки']}
            user = User(username=user_name, password=password, status=1)
            db.session.add(user)
            db.session.commit()
            database.update(request.user_id, user_name, 'user_name')
            database.update(request.user_id, 'first')
            return message_return(response, user_storage, 'Добро пожаловать!')

    if database.get_session(request.user_id, 'status_action')[0] == 'login' or input_message in ['войти']:
        user_storage = {"suggests": ['Помощь']}
        return message_return(response, user_storage,
                              'Привет! Чтобы войти в систему напиши свой индивидуальный логин и пароль через пробел.')

    buttons, user_storage = get_suggests(user_storage)
    return message_error(response, user_storage,
                         ['Конфуз;) Я ещё в разработке', 'Ой, сейчас исправлю)',
                          'Ой, неполадочка)', 'Прости, что ты это увидел:| Попробуй ещё раз',
                          'Прости, я ещё не всё знаю. Что ты там говорил?'])
