from datetime import date

from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    DatesAreIncorrectException,
    RoomNotFoundException,
    DataProcessingErrorsException,
)
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAddRequest, RoomAdd, RoomPatchRequest, RoomPatch, Room
from src.services.base import BaseService
from src.services.hotels import HotelServices


class RoomServices(BaseService):
    async def get_filtered_by_time(
        self,
        hotel_id: int,
        date_from: date,
        date_to: date,
    ):
        try:
            check_date_to_after_date_from(date_from, date_to)
        except DatesAreIncorrectException as ex:
            raise DatesAreIncorrectException from ex
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        try:
            return await self.db.rooms.get_filtered_by_time(
                hotel_id=hotel_id, date_from=date_from, date_to=date_to
            )
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex

    async def get_one_with_rels(self, hotel_id: int, room_id: int):
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        try:
            return await self.db.rooms.get_one_with_rels(hotel_id=hotel_id, id=room_id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex

    async def create_room(self, hotel_id: int, room_data: RoomAddRequest):
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            room = await self.db.rooms.add(_room_data)
            if room_data.facilities_ids is not None:
                room_facilities_data = [
                    RoomsFacilityAdd(room_id=room.id, facility_id=f_id)
                    for f_id in room_data.facilities_ids
                ]
                await self.db.rooms_facilities.add_bulk(room_facilities_data)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def edit_room(self, hotel_id: int, room_id: int, room_data: RoomAddRequest):
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(hotel_id)
        _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
        try:
            await self.db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
            await self.db.rooms_facilities.edit_facility(
                room_id, facility_id=room_data.facilities_ids
            )
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def patch_room(
        self, hotel_id: int, room_id: int, room_data: RoomPatchRequest
    ):
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(hotel_id)
        _room_data = RoomPatch(
            hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True)
        )
        try:
            await self.db.rooms.edit(_room_data, id=room_id, exclude_unset=True)
            if room_data.facilities_ids:
                await self.db.rooms_facilities.edit_facility(
                    room_id=room_id, facility_id=room_data.facilities_ids
                )
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def delete_room(self, hotel_id: int, room_id: int):
        await HotelServices(self.db).get_hotel_with_check(hotel_id)
        await self.get_room_with_check(hotel_id)
        try:
            await self.db.rooms.delete(hotel_id=hotel_id, id=room_id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def get_room_with_check(self, room_id: int) -> Room:
        try:
            return await self.db.rooms.get_one(id=room_id)
        except ObjectNotFoundException as ex:
            raise RoomNotFoundException from ex
