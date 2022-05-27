import telebot
from telebot import types
import json
import requests

token = '5309566375:AAH0VgTM1-d8e0FQOlUZlUZIafRwSmxn1Nc'
bot = telebot.TeleBot(token)


class User:
    login = None
    password = None


user = User()


@bot.message_handler(commands = ['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/Авторизация')
    btn2 = types.KeyboardButton('получить расписание')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


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
        mess = bot.send_message(message.chat.id, 'Подтвердите авторизацию')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        markup.add(btn1, btn2)
        bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)
        bot.register_next_step_handler(mess, auto)
        print(user.login)
    except Exception as e:
        bot.reply_to(message, 'Упс! Пароль не принят! Попробуй еще раз!')


def auto(message):
    print(user.login, user.password)
    data = {"login": user.login, "password": user.password}
    js_auto = json.dumps(data)
    api = 'https://api.muiv-timetable.cf/api/'
    groups_list = requests.post(api+"auto", data=js_auto)
    print(groups_list.text)
    print(groups_list)
    print(js_auto)


file = open('shedulerData02.05.22_08.05.22.json', encoding='utf-8')
d = file.read()
data = json.loads(d)


@bot.message_handler(content_types=['text'])
def mess(message):
    get_message_bot = message.text.strip().lower()
    if get_message_bot == 'получить расписание':
        for item in data:
            sheld = data['days'][0]["Schedulers"]
            leight = len(data['days'][0]["Schedulers"])
            i = 0
            work_date_name = (data['days'][0]["Work_Date_Name"])
            day = (data['days'][0]["workDay"])
            day_text = ('Расписание на ' + work_date_name + ', ' + day + ': \n')
            bot.send_message(message.chat.id, " " + day_text)
            while i < leight:
                tutor = (sheld[i]["Tutor"])
                para_name = (sheld[i]["Area"])
                workType = (sheld[i]["WorkType"])
                place = (sheld[i]["Place"])
                workStart = (sheld[i]["WorkStart"])
                workEnd = (sheld[i]["WorkEnd"])
                comment = (sheld[i]["Comment"])
                totalizer = (sheld[i]["Totalizer"])
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


bot.polling(none_stop=True)
