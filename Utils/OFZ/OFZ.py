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
    __MAX_STEP_VALUE = 5

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
            return "Введите номинал ОФЗ"
        if self.__step == self.__STEP_WAIT_COUPON:
            return "Введите значение купона"
        if self.__step == self.__STEP_WAIT_NUMBER_OF_COUPON:
            return "Введите кол-во купонов, оставшихся к выплате"
        if self.__step == self.__STEP_WAIT_ACCUMULATES_COUPON_INCOME:
            return "Введите накопленный купонный доход"
        if self.__step == self.__STEP_WAIT_TAX:
            return "Введите текущую цену ОФЗ"

    def add_step(self, value):
        print("начат следующий шаг")
        if self.__step == self.__STEP_WAIT_NAME:
            self.__ofz_name = str(value)
        if self.__step == self.__STEP_WAIT_NOMINAL:
            self.__nominal = float(value)
        if self.__step == self.__STEP_WAIT_COUPON:
            self.__coupon = float(value)
        if self.__step == self.__STEP_WAIT_NUMBER_OF_COUPON:
            self.__number_of_coupons = int(value)
        if self.__step == self.__STEP_WAIT_ACCUMULATES_COUPON_INCOME:
            self.__accumulated_coupon_income = float(value)
        if self.__step == self.__STEP_WAIT_TAX:
            self.__tax = float(value)
        self.__step = self.__step + 1

        if self.__step <= self.__MAX_STEP_VALUE:
            return True
        else:
            return False

    def match_ofz(self):
        plus = float(self.__nominal) + float(self.__coupon)*int(self.__number_of_coupons)
        minus = float(self.__tax) + float(self.__accumulated_coupon_income) + float(self.__tax)*0.01*0.3 + float(self.__coupon)*0.13
        result = plus - minus
        return result