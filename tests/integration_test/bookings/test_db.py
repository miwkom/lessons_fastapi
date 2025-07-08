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
    await db.bookings.add(booking_data)


    booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)

    assert booking is not None
    assert booking.date_from == date(year=2025, month=11, day=10)
    assert booking.date_to == date(year=2026, month=1, day=20)
    assert booking.price == 100


    update_booking_data = BookingAdd(
        user_id=user_id,
        room_id=room_id,
        date_from=date(year=2022, month=4, day=10),
        date_to=date(year=2024, month=6, day=20),
        price=456,
    )
    await db.bookings.edit(data=update_booking_data, user_id=user_id, room_id=room_id)

    booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking is not None
    assert booking.date_from == date(year=2022, month=4, day=10)
    assert booking.date_to == date(year=2024, month=6, day=20)
    assert booking.price == 456


    await db.bookings.delete(user_id=user_id, room_id=room_id)

    booking = await db.bookings.get_one_or_none(user_id=user_id, room_id=room_id)
    assert booking is None

    await db.commit()

