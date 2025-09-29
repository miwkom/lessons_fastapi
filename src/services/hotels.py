from datetime import date
from typing import Optional

from src.api.dependencies import PaginationDep
from src.exceptions import (
    check_date_to_after_date_from,
    ObjectNotFoundException,
    HotelNotFoundException,
    DataProcessingErrorsException,
    DatesAreIncorrectException,
)
from src.schemas.hotels import HotelAdd, Hotel
from src.services.base import BaseService


class HotelServices(BaseService):
    async def get_filtered_by_time(
        self,
        pagination: PaginationDep,
        title: Optional[str],
        location: Optional[str],
        date_from: date,
        date_to: date,
    ):
        per_page = pagination.per_page or 5
        try:
            check_date_to_after_date_from(date_from, date_to)
        except DatesAreIncorrectException as ex:
            raise DatesAreIncorrectException from ex
        try:
            hotels = await self.db.hotels.get_filtered_by_time(
                date_from=date_from,
                date_to=date_to,
                title=title,
                location=location,
                limit=per_page,
                offset=per_page * (pagination.page - 1),
            )
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        return hotels

    async def get_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        return await self.db.hotels.get_one(id=hotel_id)

    async def add_hotel(self, hotel_data: HotelAdd):
        try:
            hotel = await self.db.hotels.add(hotel_data)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()
        return hotel

    async def edit_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.get_hotel_with_check(hotel_id)
        try:
            await self.db.hotels.edit(hotel_data, id=hotel_id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def patch_hotel(self, hotel_id: int, hotel_data: HotelAdd):
        await self.get_hotel_with_check(hotel_id)
        try:
            await self.db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def delete_hotel(self, hotel_id: int):
        await self.get_hotel_with_check(hotel_id)
        try:
            await self.db.hotels.delete(id=hotel_id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()

    async def get_hotel_with_check(self, hotel_id: int) -> Hotel:
        try:
            await self.db.hotels.get_one(id=hotel_id)
        except ObjectNotFoundException as ex:
            raise HotelNotFoundException from ex
