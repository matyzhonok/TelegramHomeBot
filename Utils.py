import time
import telebot
import pytz
import config


def sendLogMessage(logMessage, logLevel, logAction = "", needInform = False):
    print("[" + time.strftime("%Y-%m-%d %X", time.localtime()) + "]" + " " +
          "[" + logLevel + "]" + " " +
          "[" + logAction + "]" + " " +
          logMessage)
    if (needInform):
        P_TIMEZONE = pytz.timezone(config.TIMEZONE)
        TIMEZONE_COMMON_NAME = config.TIMEZONE_COMMON_NAME
        bot = telebot.TeleBot(config.TOKEN)  # указываем токен конкретного бота
        bot.send_message(291335695,
                         "[" + time.strftime("%Y-%m-%d %X", time.localtime()) + "]" + " " +
                         "[" + logLevel + "]" + " " +
                         "[" + logAction + "]" + " " +
                         logMessage)