from datetime import date
from http.client import HTTPException


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


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise HTTPException(status_code=422, detail="Некорректно введенная дата")


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = "None"

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"
