from sqlalchemy import select

from src.models.hotels import HotelsModel
from src.repositories.base import BaseRepository
from src.schemas.hotels import Hotel


class HotelsRepository(BaseRepository):
    model = HotelsModel
    schema = Hotel

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ) -> list[Hotel]:
        query = select(HotelsModel)
        if title:
            query = query.filter(HotelsModel.title.ilike(f"%{title}%"))
        if location:
            query = query.filter(HotelsModel.location.ilike(f"%{location}%"))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )

        result = await self.session.execute(query)
        return [Hotel.model_validate(hotel) for hotel in result.scalars().all()]
