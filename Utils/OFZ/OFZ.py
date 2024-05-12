from Utils.send_one_message import sendOneMessage

class OFZ:
    """Класс обработки расчёта ОФЗ"""

    # Шаги по вводу данных
    __STEP_WAIT_NAME = 0
    __STEP_WAIT_NOMINAL = 1
    __STEP_WAIT_COUPON = 2
    __STEP_WAIT_NUMBER_OF_COUPON = 3
    __STEP_WAIT_ACCUMULATES_COUPON_INCOME = 4
    __STEP_WAIT_TAX = 5

    __step = -1 # Какой шаг ввода информации
    __ofz_name = ""
    __nominal = 0 # Номинал ОФЗ
    __coupon = 0 # Размер купона
    __number_of_coupons = 0 # Осталось купонов к выплате
    __accumulated_coupon_income = 0 # Накопленный купонный доход
    __tax = 0.13 # Налоговая ставка на купонный доход

    def __init__(self):
        self.__step = 0



    def get_step_welcome_text(self):
        if self.__step == self.__STEP_WAIT_NAME:
            return "Введите название ОФЗ"
        if self.__step == self.__STEP_WAIT_NOMINAL:
            return "Введите номинал купона"
        if self.__step == self.__STEP_WAIT_COUPON:
            return ""
        if self.__step == self.__STEP_WAIT_NUMBER_OF_COUPON:
            return ""
        if self.__step == self.__STEP_WAIT_ACCUMULATES_COUPON_INCOME:
            return ""
        if self.__step == self.__STEP_WAIT_TAX:
            return ""

    def add_step(self, value):
        print("начат следующий шаг")
        if self.__step == self.__STEP_WAIT_NAME:
            self.__ofz_name = value
            self.__step = self.__step + 1
            return True
        if self.__step == self.__STEP_WAIT_NOMINAL:
            self.__nominal = value
            self.__step = self.__step + 1
            return True
        if self.__step == self.__STEP_WAIT_COUPON:
            self.__coupon = value
            self.__step = self.__step + 1
            return True
