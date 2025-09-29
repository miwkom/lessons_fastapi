from src.exceptions import (
    DataProcessingErrorsException,
    ObjectNotFoundException,
    FacilitiesNotFoundException,
)
from src.schemas.facilities import Facility, FacilityAdd
from src.services.base import BaseService
from src.tasks.tasks import test_task


class FacilitiesService(BaseService):
    async def get_facilities(self):
        try:
            facilities = await self.db.facilities.get_all()
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        return facilities

    async def create_facility(self, data: FacilityAdd) -> Facility:
        try:
            facilities = await self.db.facilities.add(data)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()
        test_task.delay()
        return facilities

    async def delete_facility(self, facilities_id: int) -> Facility:
        try:
            await self.db.facilities.get_one(id=facilities_id)
        except ObjectNotFoundException as ex:
            raise FacilitiesNotFoundException from ex
        try:
            await self.db.facilities.delete(id=facilities_id)
        except DataProcessingErrorsException as ex:
            raise DataProcessingErrorsException from ex
        await self.db.commit()
