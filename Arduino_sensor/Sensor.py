# Класс одного сенсора

class Sensor:

    def __init__(self, id, name):
        self.sensor_id = id
        self.sensor_name = name
        print("Создан один сенсор, id=\"" + str(id) + "\" name=\"" + name + "\"")

    @property
    def name(self):
        return self.sensor_name
