##
# Класс для обработки команд по сенсорам
##
import json
import Arduino_sensor.Sensor

class Sensors:

    def __new__(cls):
        # Перекрываем создание объекта класса
        if not hasattr(cls, 'instance'):
            cls.instance = super(Sensors, cls).__new__(cls)
        return cls.instance

    def config(self):
        sensors = {}
        print("Сработала команда на конфигурацию сенсоров")
        text = json.load(open('./sensor_config/sensors.json', 'r', encoding='utf-8'))
        for txt in text['sensor_lib']:
            sensors[txt["id"]] = Arduino_sensor.Sensor.Sensor(txt["id"], txt["name"])
