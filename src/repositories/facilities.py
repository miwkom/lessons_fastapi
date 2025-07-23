from sqlalchemy import select, insert, delete

from src.models.facilities import FacilitiesModel, RoomsFacilitiesModel
from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import FacilityDataMapper, RoomFacilityDataMapper


class FacilitiesRepository(BaseRepository):
    model = FacilitiesModel
    mapper = FacilityDataMapper


class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesModel
    mapper = RoomFacilityDataMapper

    async def edit_facility(
        self,
        room_id: int,
        facility_id: list[int],
    ) -> None:
        get_current_facilities_ids_query = (
            select(self.model.facility_id)
            .select_from(RoomsFacilitiesModel)
            .filter_by(room_id=room_id)
        )
        res = await self.session.execute(get_current_facilities_ids_query)
        current_facilities_ids: list[int] = res.scalars().all()

        to_add = set(facility_id) - set(current_facilities_ids)
        to_delete = set(current_facilities_ids) - set(facility_id)

        if to_add:
            add_m2m_facilities_stmt = insert(self.model).values(
                [{"room_id": room_id, "facility_id": f_id} for f_id in to_add]
            )
            await self.session.execute(add_m2m_facilities_stmt)

        if to_delete:
            delete_m2m_facilities_stmt = delete(self.model).filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(to_add),
            )
            await self.session.execute(delete_m2m_facilities_stmt)
