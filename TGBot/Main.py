import telebot
from telebot import types
import json

token = '5309566375:AAH0VgTM1-d8e0FQOlUZlUZIafRwSmxn1Nc'
bot = telebot.TeleBot(token)
@bot.message_handler(commands = ['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} '
    bot.send_message(message.chat.id, mess, parse_mode = 'html')
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
    btn1 = types.KeyboardButton('получить расписание')
    # btn2 = types.KeyboardButton('Ввести комментарий')
    markup.add(btn1)
    bot.send_message(message.chat.id, 'Воспользуйся кнопками!', reply_markup=markup)

# @bot.message_handler(content_types = ['text'])
# def mess(message):
#      get_message_bot = message.text.strip().lower()
     # if get_message_bot == 'получить расписание':
     #    bot.send_message(message.chat.id, 'Введите дату')
     # elif get_message_bot == '14.05.2022':
     #    bot.send_message(message.chat.id, 'Выберите факультет')
     #    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
     #    btn1 = types.KeyboardButton('Факультет Информационных технологий')
     #    btn2 = types.KeyboardButton('Факультет Управления')
     #    btn3 = types.KeyboardButton('Факультет Экономики')
     #    btn4 = types.KeyboardButton('Юридический факультет')

     #    markup.add(btn1, btn2, btn3, btn4)
     #    bot.send_message(message.chat.id, 'Воспользуйся кнопками!', reply_markup=markup)
     # if get_message_bot == 'факультет информационных технологий':
     #    bot.send_message(message.chat.id, 'Введите группу')

     # else:
     #      markup = types.ReplyKeyboardMarkup(resize_keyboard = True, row_width=1)
     #      btn1 = types.KeyboardButton('Получить расписание')
     #
     #      markup.add(btn1)
     #      bot.send_message(message.chat.id, 'Воспользуйся кнопками!', reply_markup=markup)

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
            while i < leight:
                tutor = (sheld[i]["Tutor"])
                Work_Date_Name = (data['days'][0]["Work_Date_Name"])
                day = (data['days'][0]["workDay"])
                para_name = (sheld[i]["Area"])
                WorkType = (sheld[i]["WorkType"])
                place = (sheld[i]["Place"])
                WorkStart = (sheld[i]["WorkStart"])
                WorkEnd = (sheld[i]["WorkEnd"])
                Comment = (sheld[i]["Comment"])
                Totalizer = (sheld[i]["Totalizer"])
                i = i + 1
                day_text = ('Расписание на ' + Work_Date_Name + ', ' + day + ': \n')
                sheld_text = ('Название занятия: ' + para_name + '\nТип: ' + WorkType + '\nНачало занятия: ' + WorkStart + '\nКонец занятия:' + WorkEnd + '\nАудитория: ' + place + '\nПреподаватель: ' + tutor + '\nКомментарий: ' + Comment +'\n')
                bot.send_message(message.chat.id, " " + day_text + sheld_text)
            break





bot.polling(none_stop=True)