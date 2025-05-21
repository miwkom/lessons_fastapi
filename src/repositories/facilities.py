from sqlalchemy import select, insert, delete

from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.base import BaseRepository
from src.schemas.facilities import Facility, RoomFacility


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    schema = Facility


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    schema = RoomFacility

    async def edit_facility(
            self,
            room_id,
            facility_id
    ):
        query = await self.session.execute(
            select(RoomsFacilitiesModel.facility_id)
            .select_from(RoomsFacilitiesModel)
            .filter_by(room_id=room_id)
        )
        current_facilities_ids = {i[0] for i in query}

        to_add = set(facility_id) - current_facilities_ids
        to_remove = current_facilities_ids - set(facility_id)

        if to_add:
            for f_id in to_add:
                await self.session.execute(
                    insert(RoomsFacilitiesModel).values(facility_id=f_id, room_id=room_id)
                )

        if to_remove:
            for f_id in to_remove:
                await self.session.execute(
                    delete(RoomsFacilitiesModel).where(
                        RoomsFacilitiesModel.facility_id == f_id,
                        RoomsFacilitiesModel.room_id == room_id
                    )
                )
