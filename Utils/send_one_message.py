import telebot
import config_local


def sendOneMessage(message, user_id):
    bot = telebot.TeleBot(config_local.TOKEN)  # указываем токен конкретного бота
    bot.send_message(user_id, message)