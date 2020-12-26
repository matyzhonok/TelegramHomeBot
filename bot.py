#!/usr/bin/python3
import telebot
import config
import config_local
import datetime
import pytz
import json
import traceback
import User
import Utils
import time
import requests

Utils.sendLogMessage("Бот запущен", "INFO", "START", True) # Выводим сообщение о начале работы бота


# Инициализируем бота:
P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
bot = telebot.TeleBot(config_local.TOKEN) # указываем токен конкретного бота

##
# Блок разбора конкретных команд бота
##

# Команда START
@bot.message_handler(commands=['start'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        bot.send_message(message.chat.id, "Авторизация пройдена успешно. \n" +
                         "Приветствую тебя, " + User.getName(message.chat.id) + "!")
        Utils.sendLogMessage("Пользователь _" + User.getName(message.chat.id) + "_ авторизировался", "INFO", "AUTH")
        return True
    bot.send_message(message.chat.id, 'Авторизация не пройдена, функционал ограничен.')
    Utils.sendLogMessage("Пользователь _" + str(message.chat.id) + "_ НЕ авторизирован.", "INFO", "AUTH", True)

# Команда HELP
@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Написать разработчику', url='telegram.me/matyzhonok'))
    keyboard.add(telebot.types.InlineKeyboardButton('Курс валют (пока не работает)', callback_data='/exchange'))
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)

# Команда EXCHANGE (курс валют)
@bot.message_handler(commands=['exchange'])
def exchange_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('EUR', callback_data='/exchange-EUR'),
        telebot.types.InlineKeyboardButton('USD', callback_data='/exchange-USD')
    )
    bot.send_message(
        message.chat.id,
        'Когда-нибудь я буду уметь высылать курсы валют... однако пока я этого не умею...\nПрости\nня',
        reply_markup=keyboard
    )

@bot.message_handler(commands=['Led_Status'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.18.101/LED=status&API=yes')
        str_led = response.text
        bot.send_message(message.chat.id, "Статус светодиода: " + str_led)
        return True

@bot.message_handler(commands=['Led_On'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.18.101/LED=ON&API=yes')
        bot.send_message(message.chat.id, "Статус запроса: " + response.status_code.__str__())
        return True

@bot.message_handler(commands=['Led_Off'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.18.101/LED=OFF&API=yes')
        bot.send_message(message.chat.id, "Статус запроса: " + response.status_code.__str__())
        return True

@bot.message_handler(commands=['Arduino_status'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.18.101/main=status&API=yes')
        bot.send_message(message.chat.id, response.text)
        return True


bot.polling(none_stop=True)