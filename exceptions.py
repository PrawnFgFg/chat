class MainException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)
        
        
class InvalidTokenException(MainException):
    detail = "Неверный токен"