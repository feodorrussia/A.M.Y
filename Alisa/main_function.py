# coding: utf-8
from __future__ import unicode_literals
from little_fuctions import *
from database_messager import *


def handle_dialog(request, response, user_storage, database):
    if not user_storage:
        user_storage = {"suggests": bop}
    input_message = request.command.lower()

    if request.user_id not in database.get_session(all=True):
        database.add_session(request.user_id)
        print(database.get_session(request.user_id))

    if database.get_session(request.user_id, 'status_action')[0] == 'login' and len(
            input_message.split()) == 2:
        user_name, password = request.command.split()
        if User.query.filter_by(username=user_name).all():  # Проверка на нового пользователя
            user = User.query.filter_by(username=user_name).first()
            if user.password == password:  # Проверка на правильность пароля
                user_storage = {'suggests': Settings.query.filter_by(id=user.id).first().bfp.split(';_;')}
                database.update(request.user_id, user_name, 'user_name')
                database.update(request.user_id, 'first')
                return message_return(response, user_storage, 'Добро пожаловать!' + new_message())
            else:  # Информирование об ошибке
                return message_return(response, user_storage,
                                      'Ошибка!) Попробуй ещё раз, но помни, логин должен быть индивидуальным!')
        else:  # Создание нового пользователя
            user_storage = {'suggests': bfp_i}
            user = User(username=user_name, password=password, status=1)
            settings = Settings(bfp=';_;'.join(bfp_i), ar_uid=0, voice=1)  # Настройки по умолчанию
            db.session.add(user)
            db.session.add(settings)
            db.session.commit()
            database.update(request.user_id, user_name, 'user_name')
            database.update(request.user_id, 'first')
            return message_return(response, user_storage, 'Добро пожаловать!')

    if database.get_session(request.user_id, 'status_action')[0] == 'login' or input_message in ['войти']:
        user_storage = {"suggests": bop}
        return message_return(response, user_storage,
                              'Привет! Чтобы войти в систему напиши свой индивидуальный логин и пароль через пробел.')

    if input_message in ewc:
        # статистика
        user_storage = {"suggests": bop}
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        user.status = 0
        db.session.commit()
        database.update(request.user_id, 'login')
        return message_return(response, user_storage,
                              'Пока! До новых встреч;)', 'Пока! До новых встреч')

    if input_message in hwc:
        # статистика
        database.update_status_system(request.user_id, 'help', 'status_action')
        output_message = 'Привет, я Эми, могу отправить твоё сообщение твоему другу, для этого, просто, скажи "Эми, напиши" и login или nickname твоего друга'
        user_storage = {'suggests': ['Мои возможности', 'Команды быстрого ввода', 'Главная']}
        database.update_status_system(request.user_id, 'working', 'status_action')
        tts = 'Привет! Я-Эми. Могу отправить твоё сообщение твоему другу. Для этого просто скажи-"Эми, напиши" и login или nickname твоего друга'
        return message_return(response, user_storage, output_message, tts)

    user_storage = {'suggests': btc}
    buttons, user_storage = get_suggests(user_storage)
    database.update(request.user_id, 'nwc')
    return message_error(response, user_storage,
                         ['Что ты имел ввиду?'])
