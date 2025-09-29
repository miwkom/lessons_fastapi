from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    AllRoomsAreBookedException,
    DataProcessingErrorsException,
    UserNotFoundException,
)
from src.schemas.bookings import BookingRequestAdd, BookingAdd
from src.services.base import BaseService


class BookingSevices(BaseService):
    async def create_booking(self, user_id: str, booking_data: BookingRequestAdd):
        try:
            room = await self.db.rooms.get_one(id=booking_data.room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
        room_price: int = room.price
        _booking_data = BookingAdd(
            user_id=user_id, price=room_price, **booking_data.model_dump()
        )
        try:
            booking = await self.db.bookings.add_booking(
                _booking_data, hotel_id=room.hotel_id
            )
        except DataProcessingErrorsException as ex:
            raise AllRoomsAreBookedException from ex
        await self.db.commit()
        return booking

    async def get_bookings(self):
        try:
            bookings = await self.db.bookings.get_all()
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        return bookings

    async def get_booking(self, user_id):
        try:
            user = await self.db.users.get_one(id=user_id)
        except ObjectNotFoundException as ex:
            raise UserNotFoundException from ex
        try:
            booking = await self.db.bookings.get_filtered(user_id=user.id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        return booking
