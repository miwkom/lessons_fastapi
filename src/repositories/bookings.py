from datetime import date

from sqlalchemy import select, func

from src.models.bookings import BookingsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import BookingDataMapper


class BookingsRepository(BaseRepository):
    model = BookingsModel
    mapper = BookingDataMapper

    async def get_bookings_with_today_checkin(self):
        query = (
            select(BookingsModel)
            .filter(BookingsModel.date_from == date.today())
        )
        res = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(booking) for booking in res.scalars().all()]

    async def add_booking(self, booking_data):
        rooms_count = (
            select(BookingsModel.room_id, func.count("*").label("rooms_booked"))
            .select_from(BookingsModel)
            .filter(
                BookingsModel.date_from <= booking_data.date_to,
                BookingsModel.date_to >= booking_data.date_from,
            )
            .group_by(BookingsModel.room_id)
            .cte(name="rooms_count")
        )
        rooms_left_table = (
            select(
                RoomsModel.id.label("room_id"),
                (RoomsModel.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left")
            )
            .select_from(RoomsModel)
            .outerjoin(rooms_count, RoomsModel.id == rooms_count.c.room_id)
            .cte(name="rooms_left_table")
        )
        query = (
            select(rooms_left_table)
            .select_from(rooms_left_table)
            .filter(rooms_left_table.c.rooms_left > 0, rooms_left_table.c.room_id == booking_data.room_id)
        )
        room = await self.session.execute(query)
        room = room.scalars().first()
        if room is None:
            raise Exception(404, "Room not found")
        booking = await self.add(booking_data)
        return booking
