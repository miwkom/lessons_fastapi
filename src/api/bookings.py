from fastapi import APIRouter, Body, HTTPException
from sqlalchemy.exc import NoResultFound

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingRequestAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("", summary="Создать бронирование")
async def create_booking(
        db: DBDep,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-01-25",
                    "date_to": "2025-02-25",
                }
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-03-25",
                    "date_to": "2025-04-25",
                }
            },
            "3": {
                "summary": "Пример 3",
                "value": {
                    "room_id": "1",
                    "date_from": "2025-05-25",
                    "date_to": "2025-06-25",
                }
            }
        }),
):
    try:
        user = await db.users.get_one_or_none(id=user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь не авторизирован")
    try:
        room = await db.rooms.get_one_or_none(id=booking_data.room_id)
        price: int = room.price
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Комната не найдена")
    _booking_data = BookingAdd(
        user_id=user.id,
        price=price,
        **booking_data.model_dump()
    )
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}


@router.get("/bookings", summary="Список бронирования")
async def get_bookings(
        db: DBDep,
):
    return await db.bookings.get_all()


@router.get("/bookings/me", summary="Бронирование пользователя")
async def get_booking(
        db: DBDep,
        user_id: UserIdDep,
):
    try:
        user = await db.users.get_one_or_none(id=user_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь не авторизирован")
    return await db.bookings.get_all(user_id=user.id)
