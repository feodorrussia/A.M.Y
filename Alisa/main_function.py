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

    if input_message in ['где я?', 'где я', 'wai']:
        return message_return(response, user_storage, database.get_session(request.user_id, 'status_action')[0])

    if database.get_session(request.user_id, 'status_action')[0] == 'login' and len(
            input_message.split()) == 2:
        user_name, password = request.command.split()
        if User.query.filter_by(username=user_name).all():  # Проверка на нового пользователя
            user = User.query.filter_by(username=user_name).first()
            if user.password == password:  # Проверка на правильность пароля
                user.status = 1
                db.session.commit()
                user_storage = {'suggests': Settings.query.filter_by(id=user.id).first().bfp.split(';_;')}
                database.update(request.user_id, user_name, 'user_name')
                database.update(request.user_id, 'working')
                return message_return(response, user_storage, 'Добро пожаловать!' + search_new_message())
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
            database.update(request.user_id, 'working')
            return message_return(response, user_storage, 'Добро пожаловать!')

    if database.get_session(request.user_id, 'status_action')[0] == 'login' or input_message in enwc or request.is_new_session:
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        settings = Settings.query.filter_by(id=user.id).first()
        if settings.ar_uid==0:
            user_storage = {"suggests": bop}
            return message_return(response, user_storage,
                              'Привет! Чтобы войти в систему напиши свой индивидуальный логин и пароль через пробел.')
        else:
            user.status = 1
            db.session.commit()
            user_storage = {
                'suggests': Settings.query.filter_by(id=user.id).first().bfp.split(';_;')}
            database.update(request.user_id, user_name, 'user_name')
            database.update(request.user_id, 'working')
            return message_return(response, user_storage,
                                  'Добро пожаловать!' + search_new_message())

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
    if input_message in cnclwc:
        output_message = 'Хорошо, рада была помочь!'
        user_storage = {'suggests': bc}
        database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)

    if input_message in gfpwc:
        if database.get_session(request.user_id, 'status_action')[0] in osc:
            user_storage = {'suggests': bop}
        else:
            user_name = database.get_session(request.user_id, 'user_name')[0]
            user = User.query.filter_by(username=user_name).first()
            user_storage = {
                'suggests': Settings.query.filter_by(id=user.id).first().bfp.split(';_;')}
        database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, "Прошу)", "Прошу")

    if input_message in hwc:
        # статистика
        output_message = 'Привет, я Эми, могу отправить твоё сообщение твоему другу, для этого, просто, скажи "Эми, напиши" и login (или nickname) твоего друга'
        user_storage = {'suggests': ['Главная']}
        database.update(request.user_id, 'working', 'status_action')
        tts = 'Привет! Я-Эми. Могу отправить твоё сообщение твоему другу. Для этого просто скажи:"Эми, напиши" и login или nickname твоего друга'
        return message_return(response, user_storage, output_message, tts)

    if input_message in stwc:
        # статистика
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        settings = Settings.query.filter_by(id=user.id).first()
        output_message = 'Привет! Здесь ты можешь включить или выключить автоматическую авторизацию при входе с того же устройства и озвучивание ответов, изменить кнопки на главной странице'
        user_storage = {'suggests': [f'''Авторизация({"вкл" if settings.ar_uid==1 else "выкл"})''', f'''Звук({"вкл" if settings.voice==1 else "выкл"})''', 'Кнопки', 'Главная']}
        database.update(request.user_id, 'settings_update', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'settings_update':
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        settings = Settings.query.filter_by(id=user.id).first()
        if 'авторизация' in input_message:
            output_message = f'''{"выкл" if settings.ar_uid==1 else "вкл"}ючить автоматическую авторизацию?'''
            user_storage = {'suggests': []}
            database.update(request.user_id, 'ar_update', 'status_action')
        if 'звук' in input_message:
            output_message = f'''{"выкл" if settings.ar_uid==1 else "вкл"}ючить звук?'''
            user_storage = {'suggests': []}
            database.update(request.user_id, 'voice_update', 'status_action')
        if 'кнопки' in input_message:
            output_message = f'''Изменить кнопки а главной странице?'''
            user_storage = {'suggests': []}
            database.update(request.user_id, 'fpb_update', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'ar_update':
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        settings = Settings.query.filter_by(id=user.id).first()
        if input_message in ywc:
            settings.ar_uid = abs(settings.ar_uid-1)
            db.session.commit()
            output_message = 'Готово!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        else:
            output_message = 'Хорошо, рада была помочь!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'voice_update':
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        settings = Settings.query.filter_by(id=user.id).first()
        if input_message in ywc:
            settings.voice = abs(settings.voice-1)
            db.session.commit()
            output_message = 'Готово!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        else:
            output_message = 'Хорошо, рада была помочь!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)


    if input_message in afwc:
        # статистика
        user_name = database.get_session(request.user_id, 'user_name')[0]
        user = User.query.filter_by(username=user_name).first()
        friends = Friend.query.filter_by(user=user.username).all()
        if friends:
            output_message = "Ваши друзья:\n" + '\n'.join([x.friend + f'({x.nickname})' if x.nickname else '' + f'{" (в сети)" if User.query.filter_by(username=x.friend).first().status == 1 else " (не в сети)"}' for x in friends])
            tts = output_message
            user_storage = {'suggests': bfc}
        else:
            output_message = "Я не нашла добавленных друзей.(\nНо ты всегда можешь их найти)"
            tts = "Я не нашла добавленных друзей.-Но ты всегда можешь их найти"
            user_storage = {'suggests': bfse}
        database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message, tts)

    if input_message in swc and \
            database.get_session(request.user_id, 'status_action')[0] not in osc or\
            input_message == 'попробовать ещё раз' and \
            database.get_session(request.user_id, 'status_action')[0] == 'searching_error':
        output_message = "Хорошо.\nСкажи мне имя его учётной записи(логин в системе)"
        user_storage = {'suggests': ['Отмена']}
        database.update(request.user_id, 'searching_user', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'searching_user':
        if request.command == database.get_session(request.user_id, 'user_name')[0]:
            output_message = "Ха-ха, очень хорошая шутка!\nА теперь давай серьёзно."
            return message_return(response, user_storage, output_message)
        friend = User.query.filter_by(username=request.command).first()
        if friend:
            output_message = f"Ура!\nЯ нашла твоего друга!\nХочешь добавить его в друзья?\n({friend.username}{' (в сети)' if friend.status == 1 else ' (не в сети)'})"
            user_storage = {'suggests': ['Да', 'Нет']}
            database.update(request.user_id, 'adding_friendship?', 'status_action')
            database.update(request.user_id, friend.username, 'recipient_name')
        else:
            output_message = "Прости, мне не удалось найти пользователя по твоему запросу("
            user_storage = {
                'suggests': ['Попробовать ещё раз', 'Отбой, давай на главную',
                             'Вернись в друзья']}
            database.update(request.user_id, 'searching_error', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'adding_friendship?':
        if input_message in ywc:
            output_message = 'Напиши имя друга(псевдоним), чтобы быстро написать ему сообщение(если не хочешь, напиши "нет")'
            user_storage = {'suggests': []}
            database.update(request.user_id, 'adding_friendship', 'status_action')
        else:
            output_message = 'Хорошо, рада была помочь!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'adding_friendship':
        user_name = database.get_session(request.user_id)
        if input_message in nwc:
            input_message = ''
        if Friend.query.filter_by(user=user_name[1]).filter_by(friend=user_name[2]).all():
            output_message = f'''Хорошая новость-{
            database.get_session(request.user_id, 'recipient_name')[
                0]} уже есть у тебя в друзьях! Написать ему?'''
            user_storage = {'suggests': ['Да', 'Нет']}
        else:
            print('!!!!!!!      lll',user_name)
            friendship = Friend(user=user_name[1], friend=user_name[2], nickname=input_message)
            db.session.add(friendship)
            db.session.commit()
            output_message = f'''Отлично! Теперь у тебя в друзьях есть {
            database.get_session(request.user_id, 'recipient_name')[0]}\nНаписать ему?'''
            user_storage = {'suggests': ['Да', 'Нет']}
        database.update(request.user_id, 'end_adding', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'end_adding':
        if input_message in ywc:
            output_message = 'Я готова, пиши сообщение!'
            user_storage = {
                'suggests': []}
            database.update(request.user_id, 'sending_letter', 'status_action')
        else:
            output_message = 'Хорошо, рада была помочь!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[
        0] == 'sending_letter':
        user = database.get_session(request.user_id)
        message = Message(username=user[1], message=request.command, recipient=user[2],
                          status=1)
        db.session.add(message)
        db.session.commit()
        output_message = 'Сообщение отправлено! Перейти к диалогу?'
        user_storage = {
            'suggests': ['Да', 'Нет']}
        database.update(request.user_id, 'dialog?', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'dialog?':
        if input_message in ywc:
            output_message = 'Хорошо, теперь ты сразу можешь видеть полученные сообщения и незамедлительно на них отвечать'
            user_storage = {
                'suggests': []}
            database.update(request.user_id, 'chatting', 'status_action')
        else:
            output_message = 'Хорошо, рада была помочь Вам!'
            user_storage = {'suggests': bc}
            database.update(request.user_id, 'working', 'status_action')
        return message_return(response, user_storage, output_message)

    if input_message == 'написать сообщение' and \
            database.get_session(request.user_id, 'status_action')[0] == 'working':
        output_message = 'Хорошо, скажи кому мне отправить сообщение'
        user_storage = {'suggests': []}
        database.update(request.user_id, 'connect_recipient', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'connect_recipient':
        if User.query.filter_by(username=request.command).first():
            output_message = 'Я готова, пиши сообщение!'
            user_storage = {
                'suggests': []}
            database.update(request.user_id, 'sending_letter', 'status_action')
            database.update(request.user_id, request.command, 'recipient_name')
        else:
            output_message = 'Я не нашла такого пользователя('
            user_storage = {
                'suggests': ['Отмена', 'Друзья', 'Группы', 'Найти', 'Помощь', 'Главная']}
        return message_return(response, user_storage, output_message)

    if 'напиши' in input_message and \
            database.get_session(request.user_id, 'status_action')[0] == 'working':
        if User.query.filter_by(username=request.command.split(' ')[-1]).first():
            output_message = 'Я готова, пиши сообщение!'
            user_storage = {
                'suggests': []}
            database.update(request.user_id, 'sending_letter', 'status_action')
            database.update(request.user_id, request.command.split(' ')[-1],
                                          'recipient_name')
        else:
            output_message = 'Я не нашла такого пользователя('
            user_storage = {
                'suggests': ib}
        return message_return(response, user_storage, output_message)

    if input_message == 'распечатать историю диалога':
        if database.get_session(request.user_id, 'status_action')[0] == 'chatting':
            user = database.get_session(request.user_id, 'user_name')[0]
            recipient = database.get_session(request.user_id, 'recipient_name')[0]
            dialog = Message.query.filter_by(username=user).filter_by(recipient=recipient).all()
            dialog += Message.query.filter_by(username=recipient).filter_by(recipient=user).all()
            dialog = sorted(dialog, key=lambda x: x.id)
            print('    dialog:!!!   ', dialog)
            output_message = ''
            if dialog:
                for message in dialog:
                    if message.username == user:
                        output_message += 'Вы: ' + message.message + '\n'
                    else:
                        output_message += message.username + ': ' + message.message + '\n'
                    message.status = 0
                db.session.commit()
            else:
                output_message = 'Ваш диалог пуст.'
            user_storage = {
                'suggests': cb}
        else:
            output_message = 'Прости, но сейчас эта функция не доступна. Чтобы увидеть историю диалога, зайди в диалог.(логично-логично)'
            user_storage = {
                'suggests': ['Перейти к лиалогу', 'Друзья', 'Группы', 'Найти', 'Помощь',
                             'Главная']}
        return message_return(response, user_storage, output_message)

    if input_message == 'перейти к диалогу':
        output_message = 'Хорошо, только скажи с кем?'
        user_storage = {'suggests': bc}
        database.update(request.user_id, 'connect_dialog', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'connect_dialog':
        if User.query.filter_by(username=request.command).first():
            database.update(request.user_id, request.command, 'recipient_name')
            output_message = 'Хорошо, теперь ты можешь сразу видеть полученные сообщения и незамедлительно на них отвечать'
            user_storage = {'suggests': cb}
        else:
            output_message = 'Я не нашла такого пользователя('
            user_storage = {
                'suggests': ib}
        database.update(request.user_id, 'chatting', 'status_action')
        return message_return(response, user_storage, output_message)

    if database.get_session(request.user_id, 'status_action')[0] == 'chatting':
        user = database.get_session(request.user_id, 'user_name')[0]
        recipient = database.get_session(request.user_id, 'recipient_name')[0]
        new_message = Message.query.filter_by(username=recipient).filter_by(recipient=user).filter_by(status=1).all()
        if input_message in uwc:
            user = User.query.filter_by(username=recipient).first()
            output_message = f'{user.username}{" (в сети)" if user.status == 1 else " (не в сети)"}'
        else:
            message = Message(username=user, message=request.command, recipient=recipient,
                              status=1)
            db.session.add(message)
            db.session.commit()
            user = User.query.filter_by(username=recipient).first()
            output_message = f'{user.username}{" (в сети)" if user.status == 1 else " (не в сети)"}'
        if new_message:
            output_message = 'Новые соообщения:\n' + '\n'.join([x.message for x in new_message])
            for i in new_message:
                i.status = 0
            db.session.commit()
        user_storage = {'suggests': cb}
        return message_return(response, user_storage, output_message)



    '''user_storage = {'suggests': btc}
    buttons, user_storage = get_suggests(user_storage)
    database.update(request.user_id, 'nwc')
    return message_error(response, user_storage,
                         ['Что ты имел ввиду?'])'''
    buttons, user_storage = get_suggests(user_storage)
    return message_error(response, user_storage,
                         ['Конфуз;) Я ещё в разработке', 'Ой, сейчас исправлю)',
                          'Ой, неполадочка)', 'Прости, что ты это увидел:| Попробуй ещё раз',
                          'Прости, я ещё не всё знаю. Что ты там говорил?'])
