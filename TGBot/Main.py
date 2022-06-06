import telebot
from telebot import types
import json
import requests

token = '5309566375:AAH0VgTM1-d8e0FQOlUZlUZIafRwSmxn1Nc'
bot = telebot.TeleBot(token)


class User:
    login = None
    password = None
    identity = None


user = User()

api = 'https://api.muiv-timetable.cf/api/'


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/Авторизация')
    btn2 = types.KeyboardButton('/Расписание')
    markup.add(btn1, btn2)
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
        data = {"token": "5447544750485050324950585257585250328077", "group_id": None}
        sched  = requests.post(api + "scheduler", json = data)
        sched_json = sched.json()
        for item in sched_json:
            #Не полностью работает. ДОБАВИТЬ ДРУГОЙ ДЕНЬ
            sheld = sched_json['timetables'][0]["schedulers"]
            leight = len(sched_json['timetables'][0]["schedulers"])
            i = 0
            work_date_name = (sched_json['timetables'][0]["work_Date_Name"])
            day = (sched_json['timetables'][0]["dayOfTheWeek"])
            day_text = ('Расписание на ' + work_date_name + ', ' + str(day) + ': \n')
            bot.send_message(message.chat.id, " " + day_text)
            while i < leight:
                tutor = (sheld[i]["tutor"])
                para_name = (sheld[i]["area"])
                workType = (sheld[i]["workType"])
                place = (sheld[i]["place"])
                workStart = (sheld[i]["workStart"])
                workEnd = (sheld[i]["workEnd"])
                comment = (sheld[i]["comment"])
                totalizer = (sheld[i]["totalizer"])
                i = i + 1
                sheld_text = (' 🕒 : ' + str(workStart) + ' ' + str(workEnd) +
                              '\n 🗓️ : ' + para_name +
                              '\n 📘 : ' + workType +
                              '\n ⛺ : ' + str(place) +
                              '\n 🧑‍🏫 : ' + tutor +
                              '\n 📝 : ' + str(comment) +
                              '\n 🧑‍💻 : ' + str(totalizer))
                bot.send_message(message.chat.id, " " + sheld_text)

            break
#Не работает
    elif message.text == 'Расписание другой группы':
        m = "Введите группу"
        bot.send_message(message.chat.id, m)
        groups = requests.get(api+"groups")
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

#
def auto(message):
    try:
        if message.text == "Да":
            user.identity = message.from_user.id
            print(user.login, user.password, user.identity)
            data = {"login": user.login, "password": user.password, "userIdentity": user.identity}
            auto = requests.post(api+"auto", json=data)
            print(auto)
            print(auto.text)
            bot.send_message(message.chat.id, 'Пытаюсь авторизировать!')
            m = "Если вы регистрируетесь впервые на этом аккаунте, Проверьте почту - вам пришло письмо с кодом подтверждения. Введите команду \"Верификация\""
            bot.send_message(message.chat.id, m)
    except Exception as e:
        bot.reply_to(message, 'Упс! Регистрация провалилась')







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
