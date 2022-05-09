import telebot
from telebot import types

token = '5344029282:AAEzMaR-UbxnvFwRR9iVo0nZbjbS9R7o-ow'
bot = telebot.TeleBot(token)
@bot.message_handler(commands=['start'])
def start(message):
    mess = f'Привет, {message.from_user.first_name} '
    bot.send_message(message.chat.id, mess, parse_mode='html')

@bot.message_handler(commands=['buttons'])
def buttons(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn1 = types.KeyboardButton('Получить расписание')
    btn2 = types.KeyboardButton('Ввести комментарий')
    markup.add(btn1, btn2)
    bot.send_message(message.chat.id, 'Ура кнопочки', reply_markup=markup)

bot.polling(none_stop=True)