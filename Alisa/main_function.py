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

    if database.get_session(request.user_id, 'status_action')[0] == 'out':
        user_storage = {"suggests": ['Помощь']}
        return message_return(response, user_storage, 'Привет!')

    buttons, user_storage = get_suggests(user_storage)
    return message_error(response, user_storage,
                         ['Конфуз;) Я ещё в разработке', 'Ой, сейчас исправлю)',
                          'Ой, неполадочка)', 'Прости, что ты это увидел:| Попробуй ещё раз',
                          'Прости, я ещё не всё знаю. Что ты там говорил?'])
