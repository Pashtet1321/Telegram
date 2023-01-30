import telebot
from telebot import types

from extensions import Converter, APIException
from config import *

def create_markup(base = None):
    markup = types.ReplyKeyboardMarkup( one_time_keyboard=True)
    buttons =[]
    for val in exchanges.keys():
        if val != base:
            buttons.append(types.KeyboardButton(val.capitalize()))

    markup.add(*buttons)
    return markup



bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands = ['start', 'help'])
def start(message: telebot.types.Message):
    text = 'Введите команду : \n название исходной валюты:\n название валюты, в которую нужно перевести: \n количество переводимой валюты:\n Увидеть список доступных валют: \n /values'
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['convert'])
def values(message: telebot.types.Message):
    text = 'Выберите валюту, для конвертации:'
    bot.send_message(message.chat.id, text, reply_markup = create_markup())
    bot.register_next_step_handler(message, base_handler)

def base_handler(message: telebot.types.Message):
    base = message.text.strip().lower()
    text = 'Выберите валюту, в которую конвертирую:'
    bot.send_message(message.chat.id, text, reply_markup = create_markup(base))
    bot.register_next_step_handler(message, sym_handler, base)

def sym_handler(message: telebot.types.Message, base):
    sym = message.text.strip()
    text = 'Выберите количества конвертируемой валюты:'
    bot.send_message(message.chat.id, text)
    bot.register_next_step_handler(message, amount_handler, base, sym)



def amount_handler(message: telebot.types.Message, base, sym):
    amount = message.text.split()
    try:
        new_price = Converter.get_price(base, sym, amount)
    except APIException as e:
        bot.send_message(message.chat.id, f"Ошибка конвертации: \n{e} ")
    else:
        text = f"Цена {amount} {base} в {sym} : {new_price}"
        bot.send_message(message.chat.id, text)

bot.polling()


