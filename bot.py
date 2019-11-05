import telebot
import config
import datetime
import pytz
import json
import traceback
import User




P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
bot = telebot.TeleBot(config.TOKEN) # указываем токен конкретного бота

@bot.message_handler(commands=['start']) # Пользователь ввёл команду /start
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        bot.send_message(message.chat.id, "Привет, " + User.getName(message.chat.id) + "! Я тебя знаю :-)")
        print("Получена команда START от авторизированного пользователя: " + User.getName(message.chat.id))
        return True
    bot.send_message(message.chat.id, 'Привет! Это семейный бот. И я тебя не смог опознать... Ты можешь посмотреть курс валют командой /exchange.')
    bot.send_message(291335695, 'Начало чата от неизвестного пользователя. ID чата: ' + str(message.chat.id))
    print('Начало чата от неизвестного пользователя. ID чата: ' + str(message.chat.id))

@bot.message_handler(commands=['help']) # Пользователь ввёл команду /help
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Написать разработчику', url='telegram.me/matyzhonok'))
    bot.send_message(
        message.chat.id,
        '1) Курс валют доступен всем пользователям по команде /exchange.\n' +
        '2) Это специализированный домашний бот, поэтому могут быть скрытые функции\n',
        reply_markup=keyboard
    )


@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('EUR', callback_data='get-EUR'),
        telebot.types.InlineKeyboardButton('USD', callback_data='get-USD')
    )
    bot.send_message(
        message.chat.id,
        'Когда-нибудь я буду уметь высылать курсы валют... однако пока я этого не умею...\nПрости\nня',
        reply_markup=keyboard
    )


bot.polling(none_stop=True)