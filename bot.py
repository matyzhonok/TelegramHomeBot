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
import Arduino_sensor.Sensors



Utils.sendLogMessage("Бот запущен", "INFO", "START", True) # Выводим сообщение о начале работы бота


# Инициализируем бота:
P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
bot = telebot.TeleBot(config_local.TOKEN) # указываем токен конкретного бота
LITLE_HOME_IP = config.LITLE_HOME_IP

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
    #keyboard.add(telebot.types.InlineKeyboardButton('Перечитать сенсоры', callback_data='Arduino_config_sensor'))
    #keyboard.add(telebot.types.InlineKeyboardButton('Статус светодиода', callback_data='Led_Status'))
    #keyboard.add(telebot.types.InlineKeyboardButton('Включить светодиод', callback_data='Led_On'),
    #             telebot.types.InlineKeyboardButton('Выключить светодиод', callback_data='Led_Off'))
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=keyboard)
    print("Меню")

@bot.message_handler(commands=['litlehome'])
def LitleHome_menu(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, "Управляем макетом домика")
    keyboard.add(telebot.types.InlineKeyboardButton('Включить свет', callback_data='LitleHome_Floor_1_Led_On'),
                 telebot.types.InlineKeyboardButton('Выключить свет', callback_data='LitleHome_Floor_1_Led_Off'))
    bot.send_message(message.chat.id, "1 этаж", reply_markup=keyboard)
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton('Включить свет', callback_data='LitleHome_Floor_2_Led_On'),
             telebot.types.InlineKeyboardButton('Выключить свет', callback_data='LitleHome_Floor_2_Led_Off'))
    bot.send_message(message.chat.id, "2 этаж", reply_markup=keyboard)

@bot.message_handler(commands=['Led_Status'])
def command_led_status(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.19.58/led/status')
        str_led = response.text
        bot.send_message(message.chat.id, "Статус светодиода: " + str_led)
        return True

@bot.message_handler(commands=['Led_On'])
def command_led_on(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.19.58/led/on')
        bot.send_message(message.chat.id, "Включение светодиода. Статус запроса: " + response.status_code.__str__())
        return True

@bot.message_handler(commands=['Led_Off'])
def command_led_off(message):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get('http://192.168.19.58/led/off')
        bot.send_message(message.chat.id, "Выключение светодиода. Статус запроса: " + response.status_code.__str__())
        return True

def command_Arduino_config_sensors(message):
    if (User.isAuthorized(message.chat.id)):
        sens.config()
        return True

def Drive_Arduino_Floor_Led(message, floor, action):
    if (User.isAuthorized(message.chat.id)):
        response = requests.get(LITLE_HOME_IP + '/Floor_' + str(floor) + '/LED/' + action)
        bot.send_message(message.chat.id, "Статус запроса: " + response.status_code.__str__())
        return True


# Обрабатываем колбэки
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Если сообщение из чата с ботом
    if call.message:
        if call.data.startswith("Floor_1"):
            print("Начинается с Floor_1")
        if call.data == "Arduino_config_sensor":
            command_Arduino_config_sensors(call.message)
            bot.answer_callback_query(call.id, text="Настройки сенсоров обновлены")
            return True
        if call.data == "Led_Status":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            command_led_status(call.message)
            help_command(call.message)
            return True
        if call.data == "Led_On":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            command_led_on(call.message)
            help_command(call.message)
            return True
        if call.data == "Led_Off":
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            command_led_off(call.message)
            help_command(call.message)
            return True
        if call.data == "Floor_1_Led_On":
            Drive_Arduino_Floor_Led(call.message,"1","ON")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+1)
            LitleHome_menu(call.message)
            return True
        if call.data == "Floor_1_Led_Off":
            Drive_Arduino_Floor_Led(call.message,"1","OFF")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id+1)
            LitleHome_menu(call.message)
            print(call.message.message_id)
            return True
        if call.data == "Floor_2_Led_On":
            Drive_Arduino_Floor_Led(call.message,"2","ON")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-2)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            LitleHome_menu(call.message)
            return True
        if call.data == "Floor_2_Led_Off":
            Drive_Arduino_Floor_Led(call.message,"2","OFF")
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-2)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            LitleHome_menu(call.message)
            return True



bot.polling(none_stop=True)