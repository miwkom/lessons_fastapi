from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy.exc import NoResultFound

from src.api.dependencies import DBDep, UserIdDep
from src.exceptions import ObjectNotFoundException, AllRoomsAreBookedException
from src.schemas.bookings import BookingAdd, BookingRequestAdd

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
        room = await db.rooms.get_one(id=booking_data.room_id)
    except ObjectNotFoundException:
        raise HTTPException(status_code=400, detail="Номер не найден")
    room_price: int = room.price
    _booking_data = BookingAdd(
        user_id=user_id, price=room_price, **booking_data.model_dump()
    )
    try:
        booking = await db.bookings.add_booking(_booking_data, hotel_id=room.hotel_id)
    except AllRoomsAreBookedException as ex:
        raise HTTPException(status_code=409, detail=ex.detail)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("/bookings", summary="Список бронирования")
@cache(expire=60)
async def get_bookings(
    db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/me", summary="Бронирование пользователя")
@cache(expire=60)
async def get_booking(
    db: DBDep,
    user_id: UserIdDep,
):
    try:
        user = await db.users.get_one_or_none(id=user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь не авторизирован")
    return await db.bookings.get_filtered(user_id=user.id)
