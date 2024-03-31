class MyException(Exception):
    def __init__(self, message="Превышено количество запросов"):
        super().__init__(message)
