from datetime import date

from src.schemas.bookings import BookingAdd


async def test_booking_crud(db):
    user_id = (await db.users.get_all())[0].id
    room_id = (await db.rooms.get_all())[0].id
    booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2025, month=11, day=10),
        date_to=date(year=2026, month=1, day=20),
        price=100,
    )
    new_booking = await db.bookings.add(booking_data)

    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert booking
    assert booking.id == new_booking.id
    assert booking.user_id == new_booking.user_id
    assert booking.room_id == new_booking.room_id

    updated_date_from = date(year=2022, month=4, day=10)
    updated_date_to = date(year=2026, month=4, day=20)
    updated_price = 456
    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=updated_date_from,
        date_to=updated_date_to,
        price=updated_price,
    )
    await db.bookings.edit(data=update_booking_data, id=new_booking.id)
    updated_booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert updated_booking
    assert updated_booking.id == new_booking.id
    assert updated_booking.date_from == updated_date_from
    assert updated_booking.date_to == updated_date_to
    assert updated_booking.price == updated_price

    await db.bookings.delete(id=new_booking.id)
    booking = await db.bookings.get_one_or_none(id=new_booking.id)
    assert not booking
