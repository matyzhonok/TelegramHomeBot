from Utils.OFZ.OFZ import OFZ
from Utils.send_one_message import sendOneMessage

class OFZ_Manager:
    """Класс для обработки запросов на расчёт ОФЗ для всех пользователей"""

    __ofz_list = {}

    def __init__(self):
        print(" - Создан объект управления ОФЗ")

    def init_ofz_for_user(self, user_id):
        self.__ofz_list[user_id] = OFZ()
        print("Создана заготовка ОФЗ для пользователя " + str(user_id))
        sendOneMessage(str(self.__ofz_list[user_id].get_step_welcome_text()), user_id)

    def new_step_for_user(self, user_id, value):
        print("Новый шаг ОФЗ для пользователя " + str(user_id) + " со значением " + str(value) + ".")
        if self.__ofz_list[user_id].add_step(value):
            sendOneMessage(str(self.__ofz_list[user_id].get_step_welcome_text()), user_id)
        else:
            sendOneMessage("Собраны все данные для расчёта ОФЗ", user_id)
            sendOneMessage("Выгода от покупки 1 ОФЗ составит: " + str(self.__ofz_list[user_id].match_ofz()), user_id)