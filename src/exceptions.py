class NabronirovalException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectNotFoundException(NabronirovalException):
    detail = "Объект не найден"


class AllRoomsAreBookedException(NabronirovalException):
    detail = "Не осталось свободных номеров"


class DataProcessingErrorsException(NabronirovalException):
    detail = "Ошибка обработки данных"


class DatesAreIncorrectException(NabronirovalException):
    detail = "Дата указана не верно"
