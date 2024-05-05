class OFZ:
    """Класс обработки расчёта ОФЗ"""
    __step = None # Какой шаг ввода информации
    __nominal_value = 0 # Номинал ОФЗ
    __coupon = 0 # Размер купона
    __number_of_coupons = 0 # Осталось купонов к выплате
    __accumulated_coupon_income = 0 # Накопленный купонный доход
    __tax = 0.13 # Налоговая ставка на купонный доход

    def __init__(self):
        self.__step = 1
        print("Создан объект ОФЗ")
