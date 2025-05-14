from fastapi import APIRouter, Body

from src.api.dependencies import DBDep, UserIdDep
from src.schemas.bookings import BookingAdd, BookingRequestAdd

router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.post("", summary="Создать бронирование")
async def create_booking(
        db: DBDep,
        room_id: int,
        user_id: UserIdDep,
        booking_data: BookingRequestAdd = Body(openapi_examples={
            "1": {
                "summary": "Пример 1",
                "value": {
                    "date_from": "2000-05-25",
                    "date_to": "2000-06-25",
                }
            },
            "2": {
                "summary": "Пример 2",
                "value": {
                    "date_from": "2015-05-25",
                    "date_to": "2016-05-25",
                }
            },
            "3": {
                "summary": "Пример 3",
                "value": {
                    "date_from": "2000-05-25",
                    "date_to": "2013-08-25",
                }
            }
        }),
):
    user = await db.users.get_one_or_none(id=user_id)
    price = 100
    _booking_data = BookingAdd(room_id=room_id, user_id=user.id, price=price, **booking_data.model_dump())
    booking = await db.bookings.add(_booking_data)
    await db.commit()
    return {"status": "OK", "data": booking}
