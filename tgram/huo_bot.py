import time
import telebot
import datetime
from telebot.types import *
from goog.account import Account

from config import access_key, secret_key, tg_token

acc = Account(access_key, secret_key)
bot = telebot.TeleBot(tg_token)


def extract_arg(arg):
    return arg.split('/game')[1]
    

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Стартуем!')


@bot.message_handler(commands=['bal'])
def info(message):
    params = {'accountType': 'spot', 'valuationCurrency': 'RUB'}
    data = acc.get_type_valuation(params)
    balance_rub = data['data']['balance'].replace('.', ',')

    bot.send_message(message.chat.id, balance_rub)


if __name__ == '__main__':
    print('Started polling')

    while True:
        try:
            bot.polling(none_stop=True)

        except Exception as e:
            print(e)
            time.sleep(3)
