#!/usr/bin/python3
import telebot
import config
import config_local
import datetime
import pytz
import json
import traceback
import User
import time
import requests
from Utils.logs import sendLogMessage
from Utils.Context import Context
from Utils.OFZ.OFZ_Manager import OFZ_Manager

sendLogMessage("Бот запущен", "INFO", "START", True) # Выводим сообщение о начале работы бота


# Инициализируем бота:
P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
bot = telebot.TeleBot(config_local.TOKEN) # указываем токен конкретного бота

print("Начальная инициализация всех необходимых объектов:")
# Инициализируем контексты
context = Context()
# Инициализируем обработчик запросов на ОФЗ
ofz_manager = OFZ_Manager()


print("Начальная инициализация завершена.")
print("---------------------")
print("")

##
# Блок разбора конкретных команд бота
##

# Команда START
@bot.message_handler(commands=['start'])
def start_command(message):
    if (User.isAuthorized(message.chat.id)):
        bot.send_message(message.chat.id, "Авторизация пройдена успешно. \n" +
                         "Приветствую тебя, " + User.getName(message.chat.id) + "!")
        sendLogMessage("Пользователь _" + User.getName(message.chat.id) + "_ авторизировался", "INFO", "AUTH")
        return True
    bot.send_message(message.chat.id, 'Авторизация не пройдена, функционал ограничен.')
    sendLogMessage("Пользователь _" + str(message.chat.id) + "_ НЕ авторизирован.", "INFO", "AUTH", True)

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

# Команда на обработку ОФЗ
@bot.message_handler(commands=['ofz'])
def help_command(message):
    context.set_context(message.chat.id, "OFZ")
    ofz_manager.init_ofz_for_user(message.chat.id)



# Обрабатываем колбэки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        print(call.data)

# А так мы обрабатываем просто текст и те команды, которые боту неизвестны
@bot.message_handler(content_types=['text'])
def processing_a_general_request(message):
    user_context = context.get_context(message.chat.id)
    if user_context == "OFZ":
        print("Контекст ОФЗ")
        if (ofz_manager.new_step_for_user(message.chat.id, message.text) == False):
            context.set_context(message.chat.id, "main")
    if user_context == "main":
        print("Контекст не установлен")
        print(str(message.chat.id) + "|" + message.text + "|" + str(context.get_context(message.chat.id)))
        bot.send_message(message.chat.id, 'Извините, я вас не понимаю.\n'
                                          'Выберите пожалуйста команду из меню.')

bot.polling(none_stop=True)