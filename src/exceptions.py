from datetime import date

from fastapi import HTTPException


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


class ObjectAlreadyExistsException(NabronirovalException):
    detail = "Объект уже существует"


class DatesAreIncorrectException(NabronirovalException):
    detail = "Дата указана не верно"


class HotelNotFoundException(NabronirovalException):
    detail = "Отель не найден"


class RoomNotFoundException(NabronirovalException):
    detail = "Номер не найден"


class UserNotFoundException(NabronirovalException):
    detail = "Пользователь не найден"


class FacilitiesNotFoundException(NabronirovalException):
    detail = "Удобство не найдено"


class UnauthorizedException(NabronirovalException):
    detail = "Ошибка авторизации"


class BookingNotFoundException(NabronirovalException):
    detail = "Бронирование не найдено"


def check_date_to_after_date_from(date_from: date, date_to: date) -> None:
    if date_to <= date_from:
        raise DatesAreIncorrectException


class NabronirovalHTTPException(HTTPException):
    status_code = 500
    detail = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class HotelNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Отель не найден"


class RoomNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Номер не найден"


class UserNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Пользователь не найден"


class FacilitiesNotFoundHTTPException(NabronirovalHTTPException):
    status_code = 404
    detail = "Удобства не найдены"


class UserAlreadyExistHTTPException(NabronirovalHTTPException):
    status_code = 403
    detail = "Пользователь уже существует"


class DataProcessingErrorsHTTPException(NabronirovalHTTPException):
    status_code = 403
    detail = "Ошибка обработки данных"


class WrongPasswordHTTPException(NabronirovalHTTPException):
    status_code = 403
    detail = "Неверный пароль"


class UnauthorizedHTTPException(NabronirovalHTTPException):
    status_code = 403
    detail = "Ошибка авторизации"


class AllRoomsAreBookedHTTPException(NabronirovalHTTPException):
    status_code = 409
    detail = "Не осталось свободных номеров"


class DatesAreIncorrectHTTPException(NabronirovalHTTPException):
    status_code = 422
    detail = "Дата указана не верно"
