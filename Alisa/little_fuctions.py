import random

API_CODE = 'dict.1.1.20190331T101514Z.9cbf4535b1122019.dbd3fb8c0fded55cd45d1f44459bbfda21d8e82a'
BASIC_REQUEST = 'https://dictionary.yandex.net/api/v1/dicservice.json/lookup?' \
                'key={API_CODE}&' \
                'lang=TRANS&' \
                'text=TEXTWORD'\
    .format(API_CODE=API_CODE)

ERRORS = {200: 'Запрос выполнен',
          401: 'Ключ API невалиден',
          402: 'Ключ API заблокирован',
          403: 'Превышено суточное ограничение на кол-во запросов',
          413: 'Превышен максимальный размер текста',
          501: 'Заданное направление перевода не поддерживается'}


def get_suggests(user_storage):
    if "suggests" in user_storage.keys():
        suggests = []
        for suggest in user_storage['suggests']:
            if type(suggest) != list:
                suggests.append({'title': suggest, 'hide': True})
            else:
                print(suggest)
                suggests.append({'title': suggest[0], "url": suggest[1], 'hide': False})
                print(suggests)
    else:
        suggests = []

    return suggests, user_storage


def message_error(response, user_storage, answer,  tts=None, voice=True):
    message = random.choice(answer)
    response.set_text(message)
    if voice:
        if not tts:
            response.set_tts(
                message + "Доступные команды: {}.".format(" ,".join(user_storage['suggests'])))
        else:
            response.set_tts(
                tts + "Доступные команды: {}.".format(" ,".join(user_storage['suggests'])))
    else:
        response.set_tts(' ')
    buttons, user_storage = get_suggests(user_storage)
    response.set_buttons(buttons)
    return response, user_storage


# Ну вот эта функция всем функциям функция, ага. Замена постоянному формированию ответа, ага, экономит 4 строчки!!
def message_return(response, user_storage, message,  tts=None, voice=True):  # ща будет магия
    response.set_text(message)
    if voice:
        if not tts:
            response.set_tts(message)
        else:
            response.set_tts(tts)
    else:
        response.set_tts(' ')
    buttons, user_storage = get_suggests(user_storage)
    response.set_buttons(buttons)
    return response, user_storage

#Эта функция будет находить непрочитанные сообщения пользователя user и возвращать соответствующую строку
def search_new_message():
    return '1'
