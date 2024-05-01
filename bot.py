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
@bot.message_handler(commands=['menu'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Написать разработчику', url='telegram.me/matyzhonok'))
    keyboard.add(telebot.types.InlineKeyboardButton('Перечитать сенсоры', callback_data='Arduino_config_sensor'))
    #keyboard.add(telebot.types.InlineKeyboardButton('Статус светодиода', callback_data='Led_Status'))
    #keyboard.add(telebot.types.InlineKeyboardButton('Включить светодиод', callback_data='Led_On'),
    #             telebot.types.InlineKeyboardButton('Выключить светодиод', callback_data='Led_Off'))
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)
    print("Меню")

# Обрабатываем колбэки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        print(call.data)

# А так мы обрабатываем просто текст
@bot.message_handler(content_types=['text'])
def lalala(message):
    print(str(message.chat.id) + "|" + message.text + "|")

bot.polling(none_stop=True)