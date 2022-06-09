import telebot
from telebot import types
import json
import requests
import re

token = '5309566375:AAH0VgTM1-d8e0FQOlUZlUZIafRwSmxn1Nc'
bot = telebot.TeleBot(token)


class User:
    login = None
    password = None
    identity = None


user = User()


class Comment:
    comm = None
    id = None
    token = None


comment = Comment()


class Totalizer():
    id = []
    token = None
    moreOrLess = True


tot = Totalizer()


class Verify():
    token = None
    email_code = None
    user_identity = None


verify = Verify()


api = 'https://api.muiv-timetable.cf/api/'


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/Авторизация')
    btn2 = types.KeyboardButton('/Расписание')
    btn3 = types.KeyboardButton('/Комментарий')
    btn4 = types.KeyboardButton('/Отметиться')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['Расписание'])
def sched(message):
    m = "Какое расписание вы хотите получить?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Мое расписание')
    btn2 = types.KeyboardButton('Расписание другой группы')
    markup.add(btn1, btn2)
    mess = bot.send_message(message.chat.id, m, reply_markup=markup)
    bot.register_next_step_handler(mess, get_sched)


def get_sched(message):
    if message.text == 'Мое расписание':
        m = "Введите токен"
        mess = bot.send_message(message.chat.id, m)
        bot.register_next_step_handler(mess, give_sched)
    elif message.text == 'Расписание другой группы':
        m = "Введите группу"
        bot.send_message(message.chat.id, m)
        groups = requests.get(api + "groups")
        groups_json = groups.json()
        for item in groups_json:
            a = groups_json['groups']
            leight = len(a)
            i = 0
            while i < leight:
                id = str(a[i]['group_id'])
                name = a[i]['group_name']
                print("id=" + id + "group name =" + name)
                i = i + 1
            break
        # for item in groups_json:
        #     a = groups_json['groups'][0]
        #     print(a)
        # group = groups_json['groups'][0]
        # print(group)

        print('fd')
    else:
        m = "Я тебя не понимаю"
        bot.send_message(message.chat.id, m)


def give_sched(message):
    token = message.text
    # data = {"token": token, "group_id": None}
    #     # sched = requests.post(api + "scheduler", json=data)
    #     # sched_json = sched.json()
    file = open('shedulerData02.05.22_08.05.22.json', encoding='utf-8')
    d = file.read()
    sched_json = json.loads(d)
    for item in sched_json:
        a = 0
        days_leigth = len(sched_json['timetables'])
        while a < days_leigth:
            sched = sched_json['timetables'][a]["schedulers"]
            leight = len(sched_json['timetables'][a]["schedulers"])
            work_date_name = (sched_json['timetables'][a]["work_Date_Name"])
            day = (sched_json['timetables'][a]["dayOfTheWeek"])
            day_text = ('Расписание на ' + work_date_name + ', ' + str(day) + ': \n')
            bot.send_message(message.chat.id, " " + day_text)
            a +=1
            i = 0
            while i < leight:
                tutor = (sched[i]["tutor"])
                para_name = (sched[i]["area"])
                workType = (sched[i]["workType"])
                place = (sched[i]["place"])
                workStart = (sched[i]["workStart"])
                workEnd = (sched[i]["workEnd"])
                comment = (sched[i]["comment"])
                totalizer = (sched[i]["totalizer"])
                id = (sched[i]["scheduler_id"])
                sched_text = (' 🕒 : ' + str(workStart) + ' ' + str(workEnd) +
                                  '\n 🗓️ : ' + para_name +
                                  '\n 📘 : ' + workType +
                                  '\n ⛺ : ' + str(place) +
                                  '\n 🧑‍🏫 : ' + tutor +
                                  '\n 📝 : ' + str(comment) +
                                  '\n 🧑‍💻 : ' + str(totalizer) +
                                  '\n id занятия: ' + str(id))
                i = i + 1
                bot.send_message(message.chat.id, '' + sched_text)
        break

    file.close()


@bot.message_handler(commands=['Комментарий'])
def comment(message):
    m = "Введите комментарий"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_comment)


def take_comment(message):
    comment.comm = message.text
    m = "Введите ID занятия"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_id_comm)


def take_id_comm(message):
    comment.id = message.text
    m = "Введите токен"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_token)


def take_token(message):
    comment.token = message.text
    m = "Оставляю комментарий"
    mess = bot.send_message(message.chat.id, m)
    data = {"comment": comment.comm,"scheduler_id": comment.id, "token": comment.token}
    comm = requests.post(api+"comment", json=data)


@bot.message_handler(commands=['Отметиться'])
def Totalizer(message):
    m = "Введите id занятия, Например: \"1 и 734 и 49\" (вплоть до пяти занятий)"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_id_total)


def take_id_total(message):
    nums = re.split(' и ', message.text, maxsplit=5)
    tot.id = nums
    print(tot.id)
    m = "Введите токен"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_token_total)


def take_token_total(message):
    tot.token = str(message.text)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Приду')
    btn2 = types.KeyboardButton('Не приду')
    markup.add(btn1, btn2,)
    m = "Придете на нее?"
    mess = bot.send_message(message.chat.id, m, parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(mess, totalize)


def totalize(message):
    if message.text == "Приду":
        tot.moreOrLess = True
    elif message.text == "Не приду":
        tot.moreOrLess = False
    data = {"moreOrLess": tot.moreOrLess, "scheduler_id": tot.id, "token": tot.token}
    totalizer = requests.post(api + "totalizer", json=data)
    if totalizer:
        m = "Принято, отмечаю"
        bot.send_message(message.chat.id, m)
    else:
        m = "Что-то пошло не так!"
        bot.send_message(message.chat.id, m)


@bot.message_handler(commands=['Авторизация'])
def autorization(message):
    mess = 'Введите логин '
    m = bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(m, take_login)


def take_login(message):
    try:
        user.login = message.text
        mess = bot.reply_to(message, 'Введите пароль!')
        bot.register_next_step_handler(mess, take_password)
    except Exception as e:
        bot.reply_to(message, 'Упс! Логин не принят! Попробуй еще раз!')


def take_password(message):
    try:
        user.password = message.text
        m = 'Подтвердите авторизацию'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        markup.add(btn1, btn2)
        mess = bot.send_message(message.chat.id, m,  reply_markup=markup)
        bot.register_next_step_handler(mess, auto)
    except Exception as e:
        bot.reply_to(message, 'Упс! Пароль не принят! Попробуй еще раз!')


def auto(message):
    try:
        if message.text == "Да":
            user.identity = str(message.from_user.id)
            print(user.login, user.password, user.identity)
            data = {"login": user.login, "password": user.password, "userIdentity": user.identity}
            auto = requests.post(api+"auto", json=data)
            token_json = auto.json()
            token = token_json['identityToken']
            print(auto)
            print(auto.text)
            if auto:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                btn1 = types.KeyboardButton('/Верификация')
                m = "Ваш токен " + token
                bot.send_message(message.chat.id, m)
                if token_json['answerOption'] == 2:
                    m1 = 'Вы авторизованы! Если Ваш токен оканчивается на \"p\", Проверьте почту - вам пришло письмо с кодом подтверждения. Пройдите верификацию.'
                    bot.send_message(message.chat.id, m1, reply_markup=markup)
            else:
                bot.send_message(message.chat.id, "Авторизация провалилась!")
    except Exception as e:
        bot.send_message(message.chat.id, 'Упс! Регистрация провалилась')


@bot.message_handler(commands=['Верификация'])
def verify(message):
    m = "Введите ваш Пре-токен. Он онканчивается на \"p\""
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_verify_token)


def take_verify_token(message):
    verify.token = message.text
    m = "Введите email-код"
    mess = bot.send_message(message.chat.id, m)
    bot.register_next_step_handler(mess, take_verify_code)


def take_verify_code(message):
    verify.email_code = message.text
    verify.user_identity = str(message.from_user.id)
    data = {"emailAutoToken": verify.token, "emailCode": verify.email_code, "userIdentity": verify.user_identity}
    verifi = requests.post(api + "verify", json=data)
    token_json = verifi.json()
    print(verifi)
    print(token_json)
    if token_json['answerOption']:
        token = token_json['token']
        m = "Верификация прошла успешно! Ваш токен:" + str(token)
        bot.send_message(message.chat.id, m)
    else:
        m = "Верификация провалилась!"
        bot.send_message(message.chat.id, m)


# @bot.message_handler(commands=['text'])
# def mess(message):
#     file = open('shedulerData02.05.22_08.05.22.json', encoding='utf-8')
#     d = file.read()
#     data = json.loads(d)
#     get_message_bot = message.text
#     if get_message_bot == 'расписаниеывфыа':
#         for item in data:
#             sheld = data['timetables'][0]["schedulers"]
#             leight = len(data['timetables'][0]["schedulers"])
#             i = 0
#             work_date_name = (data['timetables'][0]["work_Date_Name"])
#             day = (data['timetables'][0]["dayOfTheWeek"])
#             day_text = ('Расписание на ' + work_date_name + ', ' + str(day) + ': \n')
#             bot.send_message(message.chat.id, " " + day_text)
#             while i < leight:
#                 tutor = (sheld[i]["tutor"])
#                 para_name = (sheld[i]["area"])
#                 workType = (sheld[i]["workType"])
#                 place = (sheld[i]["place"])
#                 workStart = (sheld[i]["workStart"])
#                 workEnd = (sheld[i]["workEnd"])
#                 comment = (sheld[i]["comment"])
#                 totalizer = (sheld[i]["totalizer"])
#                 i = i + 1
#                 sheld_text = (' 🕒 : ' + str(workStart) + ' ' + str(workEnd) +
#                               '\n 🗓️ : ' + para_name +
#                               '\n 📘 : ' + workType +
#                               '\n ⛺ : ' + str(place) +
#                               '\n 🧑‍🏫 : ' + tutor +
#                               '\n 📝 : ' + str(comment) +
#                               '\n 🧑‍💻 : ' + str(totalizer))
#                 bot.send_message(message.chat.id, " " + sheld_text)
#                 print(sheld_text)
#
#             break


bot.polling(none_stop=True)
