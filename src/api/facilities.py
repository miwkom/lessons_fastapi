from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

router = APIRouter(prefix="/facilities", tags=["Удобства и услуги"])


@router.get("", summary="Список удобств и услуг")
@cache(expire=60)
async def get_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("", summary="Создать удобство или услугу")
async def create_facility(
        db: DBDep,
        facilities_data: FacilityAdd = Body(openapi_examples={
            "1": {"summary": "Wifi",
                  "value": {
                      "title": "Wifi"}
                  },
            "2": {"summary": "Parking",
                  "value": {
                      "title": "Parking"}
                  },
            "3": {"summary": "Balcony",
                  "value": {
                      "title": "Balcony"}
                  },
            "4": {"summary": "Conditioner",
                  "value": {
                      "title": "Conditioner"}
                  },
        })
):
    facilities = await db.facilities.add(facilities_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facilities}


@router.delete("/{facilities_id}", summary="Удалить удобство или услугу")
async def delete_facility(
        db: DBDep,
        facilities_id: int
):
    await db.facilities.delete(id=facilities_id)
    await db.commit()
    return {"status": "OK"}
