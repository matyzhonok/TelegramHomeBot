import telebot
import config
import datetime
import pytz
import traceback
import User

P_TIMEZONE = pytz.timezone(config.TIMEZONE)
TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
bot = telebot.TeleBot(config.TOKEN) # указываем токен конкретного бота

mess = "1. Ты теперь авторизированный пользователь.\n2. А ещё мой хозяин тестирует массовую рассылку единичного сообщения"

userList = User.getUserList()

for user_id, user_name in userList.items():
    bot.send_message(user_id, "Привет, " + user_name + "! У меня для тебя есть сообщение!")
    bot.send_message(user_id, mess)
    print("Сообщение для " + user_name + " отправлено")