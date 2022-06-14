import telebot
from keyboa.keyboards import keyboa_maker
from telebot import types
import requests
import re

token = '5309566375:AAH0VgTM1-d8e0FQOlUZlUZIafRwSmxn1Nc'
bot = telebot.TeleBot(token)


class User:
    login = None
    password = None
    identity = None


user = User()


@bot.message_handler(commands=['token'])
def autorization(message):
    mess = 'Введите логин от Личного кабинета. Твое сообщение удалится, чтоб никто его не прочитал '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Отмена')
    markup.add(btn1)
    m = bot.send_message(message.chat.id, mess, reply_markup=markup)
    bot.register_next_step_handler(m, take_login)


def take_login(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Отмена')
        markup.add(btn1)
        user.login = message.text
        bot.delete_message(message.chat.id, message.id)
        mess = bot.send_message(message.chat.id,
                                'Введите пароль от Личного кабинета. Твое сообщение удалится, чтоб никто его не прочитал',
                                reply_markup=markup)
        bot.register_next_step_handler(mess, take_password)


def take_password(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Отмена')
        markup.add(btn1)
        user.password = message.text
        bot.delete_message(message.chat.id, message.id)
        m = 'Подтвердите авторизацию'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Да')
        btn2 = types.KeyboardButton('Нет')
        markup.add(btn1, btn2)
        mess = bot.send_message(message.chat.id, m, reply_markup=markup)
        bot.register_next_step_handler(mess, auto)


def auto(message):
    if message.text == "Нет":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        if message.text == "Да":
            user.identity = str(message.from_user.id)
            data = {"login": user.login, "password": user.password, "userIdentity": user.identity}
            auto = requests.post(api + "auto", json=data)
            if auto:
                token_json = auto.json()
                token = token_json['identityToken']
                user.token = token
                if token != None:
                    m = "Авторизация завершена!"
                    bot.send_message(message.chat.id, m)
                if token_json['autoAnswerOption'] == 2:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
                    btn1 = types.KeyboardButton('/verification')
                    markup.add(btn1)
                    m1 = 'Вы авторизованы! Если вы впервые авторизируетесь с этого аккаунта, роверьте почту - вам пришло письмо ' \
                         'с кодом подтверждения. Пройдите верификацию. '
                    bot.send_message(message.chat.id, m1, reply_markup=markup)
                if token_json['autoAnswerOption'] == 1:
                    m2 = 'Неверный логин или пароль!'
                    bot.send_message(message.chat.id, m2)

class Verify():
    token = None
    email_code = None
    user_identity = None


verify = Verify()


@bot.message_handler(commands=['verification'])
def verify(message):
    try:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Отмена')
        markup.add(btn1)
        verify.token = user.token
        m = "Введите email-код"
        mess = bot.send_message(message.chat.id, m, reply_markup=markup)
        bot.register_next_step_handler(mess, take_verify_code)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так! Пройдите авторизацию повторно")

def take_verify_code(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        verify.email_code = message.text
        verify.user_identity = str(message.from_user.id)
        data = {"emailAutoToken": verify.token, "emailCode": verify.email_code, "userIdentity": verify.user_identity}
        verifi = requests.post(api + "verify", json=data)
        token_json = verifi.json()
        if verifi:
            if token_json['verifyAnswerOption']:
                token = token_json['token']
                m = "Верификация прошла успешно! Ваш токен:" + str(token)
                bot.send_message(message.chat.id, m)
            else:
                m = "Верификация провалилась! Проверьте правильность ввода!"
                bot.send_message(message.chat.id, m)
        else:
            m = "Возможно, вы ввели что-то не то! Попробуйте заново!"
            bot.send_message(message.chat.id, m)


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




api = 'https://api.muiv-timetable.cf/api/'


def print_schedluer(sched_json, message):
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
            a += 1
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


def groups1(call):
    d = requests.get(api + 'groups')
    groups_json = d.json()
    groups_leight = len(groups_json['groups'])
    i = 0
    while i < groups_leight:
        a = groups_json['groups'][i]
        for key, value in a.items():
            mess = call.data
            if value == mess:
                b = a["group_id"]
                data = {"token": None, "group_id": b}
                sched = requests.post(api + "scheduler", json=data)
                sched_json = sched.json()
                print_schedluer(sched_json=sched_json, message=call.message)
        i = i + 1


def re_call(call, year, group_name):
    year = year
    group_name = group_name
    group_list = requests.get(api + 'groups')
    groups_json = group_list.json()
    i = -1
    leigh = len(groups_json['groups'])
    list_of_value = []
    group_list = requests.get(api + 'groups')
    groups_json = group_list.json()
    i = -1
    leigh = len(groups_json['groups'])
    list_of_value = []
    list_of_group = []
    while i < (leigh - 1):
        i = i + 1
        if i > leigh:
            break
        else:
            value = groups_json['groups'][i]['group_name']
            result = re.search(year, value)
            if result:
                list_of_value.append(value)
                result1 = re.search(group_name, value)
                if result1:
                    list_of_group.append(value)
    list_of_group.append('Назад')
    text = "Выберите группу:"
    kb_groups = keyboa_maker(items=list_of_group, items_in_row=3, copy_text_to_callback=True)
    bot.edit_message_text(
        chat_id=call.message.chat.id, reply_markup=kb_groups, message_id=call.message.id,
        text=text)


@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name}! Я помогу тебе найти твое расписание. Если ты здесь впервые' \
           f' - пройди авторизацию. Ты также можешь отметиться на занятии,' \
           f' однако тебе нужен будет Id занятия - найди его в расписании . Если ты староста группы, ты можешь ' \
           f'оставить комментарий к занятию.  '
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('/token')
    btn2 = types.KeyboardButton('/scheduler')
    btn3 = types.KeyboardButton('/comment')
    btn4 = types.KeyboardButton('/check_in')
    markup.add(btn1, btn2, btn3, btn4)
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['scheduler'])
def sched(message):
    m = "Какое расписание вы хотите получить?"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Мое расписание')
    btn2 = types.KeyboardButton('Расписание другой группы')
    markup.add(btn1, btn2)
    mess = bot.send_message(message.chat.id, m, reply_markup=markup)
    bot.register_next_step_handler(mess, get_sched)


def get_sched(message):
    try:
        if message.text == 'Мое расписание':
            token = user.token
            data = {"token": token, "group_id": None}
            sched = requests.post(api + "scheduler", json=data)
            sched_json = sched.json()
            print_schedluer(sched_json=sched_json, message=message)
            bot.send_message(message.chat.id, "Что-то пошло не так! Проверьте логин")
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        elif message.text == 'Расписание другой группы':
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("5 курс", callback_data="2017")
            btn2 = types.InlineKeyboardButton("4 курс", callback_data="2018")
            btn3 = types.InlineKeyboardButton("3 курс", callback_data="2019")
            btn4 = types.InlineKeyboardButton("2 курс", callback_data="2020")
            btn5 = types.InlineKeyboardButton("1 курс", callback_data="2021")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            m = "Выберите курс"
            bot.send_message(message.chat.id, m, reply_markup=markup)
        else:
            m = "Я тебя не понимаю"
            bot.send_message(message.chat.id, m)
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так! Пройдите авторизацию повторно")


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        text = "Выберите группу:"
        if call.data == "2017":
            group_list = requests.get(api + 'groups')
            groups_json = group_list.json()
            i = -1
            leigh = len(groups_json['groups'])
            list_of_value = []
            while i < (leigh - 1):
                i = i + 1
                if i > leigh:
                    break
                else:
                    value = groups_json['groups'][i]['group_name']
                    result = re.search(r'-17', value)
                    if result:
                        list_of_value.append(value)
            list_of_value.append("Назад")
            text = "Выберите группу:"
            kb_groups = keyboa_maker(items=list_of_value, items_in_row=3, copy_text_to_callback=True)
            bot.edit_message_text(
                chat_id=call.message.chat.id, reply_markup=kb_groups, message_id=call.message.id,
                text=text)
            groups1(call=call)

        elif call.data == "2018":
            markup = types.InlineKeyboardMarkup(row_width=2)
            btn1 = types.InlineKeyboardButton("УЗД", callback_data="УЗД-18")
            btn2 = types.InlineKeyboardButton("ЭЗД", callback_data="ЭЗД-18")
            btn3 = types.InlineKeyboardButton("КДБ", callback_data="КДБ-18")
            btn4 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-18")
            btn5 = types.InlineKeyboardButton("УД", callback_data="УД-18")
            btn6 = types.InlineKeyboardButton("ЮД", callback_data="ЮД-18")
            btn7 = types.InlineKeyboardButton("РЮ", callback_data="РЮ-18")
            btn28 = types.InlineKeyboardButton("Назад", callback_data="Назад")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7).add(btn28)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text,
                                  reply_markup=markup)
        elif call.data == 'УЗД-18':
            re_call(call, year=r'-18', group_name=r'УЗД')
        elif call.data == 'ЭЗД-18':
            re_call(call, year=r'-18', group_name=r'ЭЗД')
        elif call.data == 'КДБ':
            re_call(call, year=r'-18', group_name=r'КДБ')
        elif call.data == 'УД-18':
            re_call(call, year=r'-18', group_name=r'УД')
        elif call.data == 'ЭД-18':
            re_call(call, year=r'-18', group_name=r'ЭД')
        elif call.data == 'ЮД-18':
            re_call(call, year=r'-18', group_name=r'ЮД')
        elif call.data == 'ЮД-18':
            re_call(call, year=r'-18', group_name=r'РЮ')
        elif call.data == "2019":
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("УЗД", callback_data="УЗД-19")
            btn2 = types.InlineKeyboardButton("ЭЗД", callback_data="ЭЗД-19")
            btn3 = types.InlineKeyboardButton("РКБ", callback_data="РКБ=19")
            btn4 = types.InlineKeyboardButton("ЮВД", callback_data="ЮВД-19")
            btn5 = types.InlineKeyboardButton("УД", callback_data="УД-19")
            btn6 = types.InlineKeyboardButton("ЮД", callback_data="ЮД-19")
            btn7 = types.InlineKeyboardButton("СП", callback_data="СП-19")
            btn9 = types.InlineKeyboardButton("АЗ", callback_data="АЗ-19")
            btn10 = types.InlineKeyboardButton("ЗБ", callback_data="ЗБ-19")
            btn11 = types.InlineKeyboardButton("КДБ", callback_data="КДБ-19")
            btn12 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-19")
            btn13 = types.InlineKeyboardButton("ИД", callback_data="ИД-19")
            btn28 = types.InlineKeyboardButton("Назад", callback_data="Назад")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn9, btn10, btn11, btn12, btn13).add(btn28)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text,
                                  reply_markup=markup)
        elif call.data == 'УЗД-19':
            re_call(call, year=r'-19', group_name=r'УЗД')
        elif call.data == 'ЭЗД-19':
            re_call(call, year=r'-19', group_name=r'ЭЗД')
        elif call.data == 'РКБ-19':
            re_call(call, year=r'-19', group_name=r'РКБ')
        elif call.data == 'ЮВД-19':
            re_call(call, year=r'-19', group_name=r'ЮВД')
        elif call.data == 'УД-19':
            re_call(call, year=r'-19', group_name=r'УД')
        elif call.data == 'ЮД-19':
            re_call(call, year=r'-19', group_name=r'УЗД')
        elif call.data == 'СП-19':
            re_call(call, year=r'-19', group_name=r'СП')
        elif call.data == 'АЗ-19':
            re_call(call, year=r'-19', group_name=r'АЗ')
        elif call.data == 'ЗБ-19':
            re_call(call, year=r'-19', group_name=r'ЗБ')
        elif call.data == 'КДБ-19':
            re_call(call, year=r'-19', group_name=r'КДБ')
        elif call.data == 'ЭД-19':
            re_call(call, year=r'-19', group_name=r'ЭД')
        elif call.data == 'ИД-19':
            re_call(call, year=r'-19', group_name=r'ИД')


        elif call.data == "2020":
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("УЗД", callback_data="УЗД-20")
            btn2 = types.InlineKeyboardButton("ЭЗД", callback_data="ЭЗД-20")
            btn3 = types.InlineKeyboardButton("КБ", callback_data="КБ=20")
            btn4 = types.InlineKeyboardButton("КЗБ", callback_data="КЗБ-20")
            btn5 = types.InlineKeyboardButton("УД", callback_data="УД-20")
            btn6 = types.InlineKeyboardButton("КДБ", callback_data="КДБ-20")
            btn7 = types.InlineKeyboardButton("РКБ", callback_data="РКБ-20")
            btn9 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-20")
            btn10 = types.InlineKeyboardButton("ПСО", callback_data="ПСО-20")
            btn11 = types.InlineKeyboardButton("КОМ", callback_data="КОМ-20")
            btn13 = types.InlineKeyboardButton("БУХ", callback_data="БУХ-20")
            btn14 = types.InlineKeyboardButton("ЮЗД", callback_data="ЮЗД-20")
            btn15 = types.InlineKeyboardButton("ЮВД", callback_data="ЮВД-20")
            btn16 = types.InlineKeyboardButton("АД", callback_data="АД-20")
            btn17 = types.InlineKeyboardButton("РД", callback_data="РД-20")
            btn18 = types.InlineKeyboardButton("СП", callback_data="СП-20")
            btn19 = types.InlineKeyboardButton("ЭЗ", callback_data="ЭЗ-20")
            btn20 = types.InlineKeyboardButton("РКЗБ", callback_data="РКЗБ-20")
            btn21 = types.InlineKeyboardButton("КВБ", callback_data="КВБ-20")
            btn22 = types.InlineKeyboardButton("ЮД", callback_data="ЮД-20")
            btn23 = types.InlineKeyboardButton("ИД", callback_data="ИД-20")
            btn24 = types.InlineKeyboardButton("УС", callback_data="УС-20")
            btn25 = types.InlineKeyboardButton("УЗ", callback_data="УЗ-20")
            btn26 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-20")
            btn27 = types.InlineKeyboardButton("ЭС", callback_data="ЭС-20")
            btn28 = types.InlineKeyboardButton("Назад", callback_data="Назад")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn9, btn10, btn11, btn13, btn14, btn15, btn16,
                       btn17, btn18, btn19, btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27).add(btn28)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text,
                                  reply_markup=markup)
        elif call.data == 'УЗД-20':
            re_call(call, year=r'-20', group_name=r'УЗД')
        elif call.data == 'ЭЗД-20':
            re_call(call, year=r'-20', group_name=r'ЭЗД')
        elif call.data == 'КБ-20':
            re_call(call, year=r'-20', group_name=r'КБ')
        elif call.data == 'КЗБ-20':
            re_call(call, year=r'-20', group_name=r'КЗБ')
        elif call.data == 'РКБ-20':
            re_call(call, year=r'-20', group_name=r'РКБ')
        elif call.data == 'ЭД-20':
            re_call(call, year=r'-20', group_name=r'ЭД')
        elif call.data == 'БУХ-20':
            re_call(call, year=r'-20', group_name=r'БУХ')
        elif call.data == 'ЮЗД-20':
            re_call(call, year=r'-20', group_name=r'ЮЗД')
        elif call.data == 'ЮВД-20':
            re_call(call, year=r'-20', group_name=r'ЮВД')
        elif call.data == 'ИД-20':
            re_call(call, year=r'-20', group_name=r'ИД')
        elif call.data == 'АД-20':
            re_call(call, year=r'-20', group_name=r'АД')
        elif call.data == 'РД-20':
            re_call(call, year=r'-20', group_name=r'РД')
        elif call.data == 'СП-20':
            re_call(call, year=r'-20', group_name=r'СП')
        elif call.data == 'ЭЗ-20':
            re_call(call, year=r'-20', group_name=r'ЭЗ')
        elif call.data == 'РКЗБ-20':
            re_call(call, year=r'-20', group_name=r'РКЗБ')
        elif call.data == 'КВБ-20':
            re_call(call, year=r'-20', group_name=r'КВБ')
        elif call.data == 'ЮД-20':
            re_call(call, year=r'-20', group_name=r'ЮД')
        elif call.data == 'ИД-20':
            re_call(call, year=r'-20', group_name=r'ИД')
        elif call.data == 'УС-20':
            re_call(call, year=r'-20', group_name=r'УС')
        elif call.data == 'УЗ-20':
            re_call(call, year=r'-20', group_name=r'УЗ')
        elif call.data == 'ЭД-20':
            re_call(call, year=r'-20', group_name=r'ЭД')
        elif call.data == 'ЭС-20':
            re_call(call, year=r'-20', group_name=r'ЭС')
        elif call.data == 'КДБ-20':
            re_call(call, year=r'-20', group_name=r'КДБ')
        elif call.data == 'УД-20':
            re_call(call, year=r'-20', group_name=r'УД')
        elif call.data == 'ПСО-20':
            re_call(call, year=r'-20', group_name=r'ПСО')
        elif call.data == 'КОМ-20':
            re_call(call, year=r'-20', group_name=r'КОМ')

        elif call.data == "2021":
            markup = types.InlineKeyboardMarkup(row_width=3)
            btn1 = types.InlineKeyboardButton("УЗД", callback_data="УЗД-20")
            btn2 = types.InlineKeyboardButton("ЭЗД", callback_data="ЭЗД-20")
            btn3 = types.InlineKeyboardButton("КБ", callback_data="КБ=20")
            btn4 = types.InlineKeyboardButton("КЗБ", callback_data="КЗБ-20")
            btn5 = types.InlineKeyboardButton("УД", callback_data="УД-20")
            btn6 = types.InlineKeyboardButton("КДБ", callback_data="КДБ-20")
            btn7 = types.InlineKeyboardButton("РКБ", callback_data="РКБ-20")
            btn9 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-20")
            btn10 = types.InlineKeyboardButton("ПСО", callback_data="ПСО-20")
            btn11 = types.InlineKeyboardButton("КОМ", callback_data="КОМ-20")
            btn12 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-20")
            btn13 = types.InlineKeyboardButton("БУХ", callback_data="БУХ-20")
            btn14 = types.InlineKeyboardButton("ЮЗД", callback_data="ЮЗД-20")
            btn15 = types.InlineKeyboardButton("ЮВД", callback_data="ЮВД-20")
            btn16 = types.InlineKeyboardButton("АД", callback_data="АД-20")
            btn17 = types.InlineKeyboardButton("РД", callback_data="РД-20")
            btn18 = types.InlineKeyboardButton("СП", callback_data="СП-20")
            btn19 = types.InlineKeyboardButton("ЭЗ", callback_data="ЭЗ-20")
            btn20 = types.InlineKeyboardButton("РКЗБ", callback_data="РКЗБ-20")
            btn21 = types.InlineKeyboardButton("КВБ", callback_data="КВБ-20")
            btn22 = types.InlineKeyboardButton("ЮД", callback_data="ЮД-20")
            btn23 = types.InlineKeyboardButton("ИД", callback_data="ИД-20")
            btn24 = types.InlineKeyboardButton("УС", callback_data="УС-20")
            btn25 = types.InlineKeyboardButton("УЗ", callback_data="УЗ-20")
            btn26 = types.InlineKeyboardButton("ЭД", callback_data="ЭД-20")
            btn27 = types.InlineKeyboardButton("ЭС", callback_data="ЭС-20")
            btn28 = types.InlineKeyboardButton("Назад", callback_data="Назад")
            markup.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn9, btn10, btn11, btn12, btn13, btn14, btn15, btn16,
                       btn17, btn18, btn19, btn20, btn21, btn22, btn23, btn24, btn25, btn26, btn27).add(btn28)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=text,
                                  reply_markup=markup)
        elif call.data == 'УЗД-21':
            re_call(call, year=r'-21', group_name=r'УЗД')
        elif call.data == 'ЭЗД-21':
            re_call(call, year=r'-21', group_name=r'ЭЗД')
        elif call.data == 'КБ-21':
            re_call(call, year=r'-21', group_name=r'КБ')
        elif call.data == 'КЗБ-21':
            re_call(call, year=r'-21', group_name=r'КЗБ')
        elif call.data == 'РКБ-21':
            re_call(call, year=r'-2', group_name=r'РКБ')
        elif call.data == 'ЭД-21':
            re_call(call, year=r'-21', group_name=r'ЭД')
        elif call.data == 'БУХ-21':
            re_call(call, year=r'-21', group_name=r'БУХ')
        elif call.data == 'ЮЗД-21':
            re_call(call, year=r'-21', group_name=r'ЮЗД')
        elif call.data == 'ЮВД-21':
            re_call(call, year=r'-21', group_name=r'ЮВД')
        elif call.data == 'ИД-21':
            re_call(call, year=r'-21', group_name=r'ИД')
        elif call.data == 'АД-21':
            re_call(call, year=r'-21', group_name=r'АД')
        elif call.data == 'РД-21':
            re_call(call, year=r'-21', group_name=r'РД')
        elif call.data == 'СП-21':
            re_call(call, year=r'-21', group_name=r'СП')
        elif call.data == 'ЭЗ-21':
            re_call(call, year=r'-21', group_name=r'ЭЗ')
        elif call.data == 'РКЗБ-21':
            re_call(call, year=r'-21', group_name=r'РКЗБ')
        elif call.data == 'КВБ-21':
            re_call(call, year=r'-21', group_name=r'КВБ')
        elif call.data == 'ЮД-21':
            re_call(call, year=r'-21', group_name=r'ЮД')
        elif call.data == 'ИД-21':
            re_call(call, year=r'-21', group_name=r'ИД')
        elif call.data == 'УС-21':
            re_call(call, year=r'-21', group_name=r'УС')
        elif call.data == 'УЗ-21':
            re_call(call, year=r'-21', group_name=r'УЗ')
        elif call.data == 'ЭД-21':
            re_call(call, year=r'-21', group_name=r'ЭД')
        elif call.data == 'ЭС-21':
            re_call(call, year=r'-21', group_name=r'ЭС')
        elif call.data == 'КДБ-21':
            re_call(call, year=r'-21', group_name=r'КДБ')
        elif call.data == 'УД-21':
            re_call(call, year=r'-21', group_name=r'УД')
        elif call.data == 'ПСО-21':
            re_call(call, year=r'-21', group_name=r'ПСО')
        elif call.data == 'КОМ-21':
            re_call(call, year=r'-21', group_name=r'КОМ')
        elif call.data == 'Назад':
            markup = types.InlineKeyboardMarkup(row_width=1)
            btn1 = types.InlineKeyboardButton("5 курс", callback_data="2017")
            btn2 = types.InlineKeyboardButton("4 курс", callback_data="2018")
            btn3 = types.InlineKeyboardButton("3 курс", callback_data="2019")
            btn4 = types.InlineKeyboardButton("2 курс", callback_data="2020")
            btn5 = types.InlineKeyboardButton("1 курс", callback_data="2021")
            markup.add(btn1, btn2, btn3, btn4, btn5)
            m = "Выберите курс"
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=m,
                                  reply_markup=markup)

        mess = call
        groups1(mess)

# КОММЕНТ И ОТМЕТКУ ИНЛАЙН КНОПКАМИ!!!!!
@bot.message_handler(commands=['comment'])
def comment(message):
    m = "Введите комментарий"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Отмена')
    markup.add(btn1)
    mess = bot.send_message(message.chat.id, m, reply_markup=markup)
    bot.register_next_step_handler(mess, take_comment)


def take_comment(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn1 = types.KeyboardButton('Отмена')
        markup.add(btn1)
        comment.comm = message.text
        m = "Введите ID занятия"
        mess = bot.send_message(message.chat.id, m, reply_markup=markup)
        bot.register_next_step_handler(mess, take_id_comm)


def take_id_comm(message):
    try:
        if message.text == "Отмена":
            bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
        else:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton('Отмена')
            markup.add(btn1)
            comment.token = user.token
            # data = {"token": comment.token, "group_id": None}
            # sched = requests.post(api + "scheduler", json=data)
            # sched_json = sched.json()
            # a = 0
            # days_leigth = len(sched_json['timetables'])
            # while a < days_leigth:
            #     sched = sched_json['timetables'][a]["schedulers"]
            #     leight = len(sched_json['timetables'][a]["schedulers"])
            #     a += 1
            #     i = 0
            #     if (message.text == sched_json['timetables'][a]["schedulers"][i]['area']):
            #         while i < leight:
            #             comm_id = (sched[i]["scheduler_id"])
            # comment.id = comm_id
            comment.id = message.text
            data = {"comment": comment.comm, "scheduler_id": comment.id, "token": comment.token}
            comm = requests.post(api + "comment", json=data)
            comm_json = comm.json()
            if comm:
                if comm_json["commentAnswerOption"]:
                    m = "Комментарий оставлен!"
                    bot.send_message(message.chat.id, m)
                if not comm_json["commentAnswerOption"]:
                    m = comm_json['commentAnswerInfo']
                    bot.send_message(message.chat.id, m)
    except:
        bot.send_message(message.chat.id, "Что-то пошло не так! Пройдите авторизацию повторно")


@bot.message_handler(commands=['check_in'])
def Totalizer(message):
    m = "Введите id занятия, Например: \"1 и 734 и 49\" (вплоть до пяти занятий)"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Отмена')
    markup.add(btn1)
    mess = bot.send_message(message.chat.id, m, reply_markup=markup)
    bot.register_next_step_handler(mess, take_id_total)


def take_id_total(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        try:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton('Отмена')
            markup.add(btn1)
            nums = re.split(' и ', message.text, maxsplit=5)
            tot.id = nums
            tot.token = user.token
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            btn1 = types.KeyboardButton('Приду')
            btn2 = types.KeyboardButton('Не приду')
            btn3 = types.KeyboardButton('Отмена')
            markup.add(btn1, btn2).add(btn3)
            m = "Придете на нее?"
            mess = bot.send_message(message.chat.id, m, parse_mode='html', reply_markup=markup)
            bot.register_next_step_handler(mess, totalize)
        except:
            bot.send_message(message.chat.id,  "Что-то пошло не так! Пройдите авторизацию повторно")

def totalize(message):
    if message.text == "Отмена":
        bot.send_message(message.chat.id, "Отменил! Введите команду для продолджения")
        bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
    else:
        if message.text == "Приду":
            tot.moreOrLess = True
        elif message.text == "Не приду":
            tot.moreOrLess = False
        data = {"moreOrLess": tot.moreOrLess, "scheduler_id": tot.id, "token": tot.token}
        totalizer = requests.post(api + "totalizer", json=data)
        totalizer_json = totalizer.json()
        if totalizer_json['totalizerAnswerOption']:
            m = "Принято, отмечаю"
            bot.send_message(message.chat.id, m)
        else:
            m = totalizer_json['totalizerAnswerInfo']
            bot.send_message(message.chat.id, m)






bot.polling(none_stop=True)
