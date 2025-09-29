from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import (
    AllRoomsAreBookedException,
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    AllRoomsAreBookedHTTPException,
    DataProcessingErrorsException,
    DataProcessingErrorsHTTPException,
    UserNotFoundException,
    UserNotFoundHTTPException,
)
from src.schemas.bookings import BookingRequestAdd
from src.services.bookings import BookingSevices

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("", summary="Создать бронирование")
async def create_booking(
    db: DBDep,
    user_id: UserIdDep,
    booking_data: BookingRequestAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-01-25",
                    "date_to": "2025-02-25",
                },
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-03-25",
                    "date_to": "2025-04-25",
                },
            },
            "3": {
                "summary": "Пример 3",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-05-25",
                    "date_to": "2025-06-25",
                },
            },
        }
    ),
):
    try:
        booking = await BookingSevices(db).create_booking(user_id, booking_data)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except AllRoomsAreBookedException as ex:
        raise AllRoomsAreBookedHTTPException from ex
    return {"status": "OK", "data": booking}


@router.get("/bookings", summary="Список бронирования")
@cache(expire=60)
async def get_bookings(
    db: DBDep,
):
    try:
        bookings = await BookingSevices(db).get_bookings()
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return bookings


@router.get("/me", summary="Бронирование пользователя")
@cache(expire=60)
async def get_booking(
    db: DBDep,
    user_id: UserIdDep,
):
    try:
        booking = await BookingSevices(db).get_booking(user_id)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except UserNotFoundException as ex:
        raise UserNotFoundHTTPException from ex
    return booking
