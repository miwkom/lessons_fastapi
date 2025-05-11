from sqlalchemy import select, insert

from src.models.hotels import HotelsModel
from src.models.rooms import RoomsModel
from src.repositories.base import BaseRepository
from src.repositories.hotels import HotelsRepository
from src.schemas.rooms import Room, RoomAdd


class RoomsRepository(BaseRepository):
    model = RoomsModel
    schema = Room

    async def get_all(self, hotel_id) -> list[Room]:
        query = select(RoomsModel)
        query = query.where(RoomsModel.hotel_id == hotel_id)
        result = await self.session.execute(query)
        return [Room.model_validate(room) for room in result.scalars().all()]

    async def add(self, data: RoomAdd):
        hotel = HotelsRepository(self.session).get_one_or_none(id=data.hotel_id)
        if hotel:
            add_data_stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
            result = await self.session.execute(add_data_stmt)
            model = result.scalars().one_or_none()
            return self.schema.model_validate(model, from_attributes=True)
        return None
