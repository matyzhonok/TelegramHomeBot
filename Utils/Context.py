class Context:
    """ Класс для сохранения контекстов разговоров с разными клиентами"""
    __contexts = {}

    def __init__(self):
        print("Инициирован контекст") # На самом деле тут делать ничего не нужно

    # Функция установки контента
    def set_context(self, user_id, context):
        self.__contexts[user_id] = context

    # Функция получения контента
    def get_context(self, user_id):
        return self.__contexts.get(user_id, "main") # Ищем контекст, если есть - взвращаем его, если нет - возвращаем main (главное меню)