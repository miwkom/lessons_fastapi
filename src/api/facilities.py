from fastapi import APIRouter, Body
from fastapi_cache.decorator import cache
from sqlalchemy.sql.coercions import expect

from src.api.dependencies import DBDep
from src.exceptions import (
    DataProcessingErrorsException,
    DataProcessingErrorsHTTPException,
    FacilitiesNotFoundException,
    FacilitiesNotFoundHTTPException,
)
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService

router = APIRouter(prefix="/facilities", tags=["Удобства и услуги"])


@router.get("", summary="Список удобств и услуг")
@cache(expire=60)
async def get_facilities(db: DBDep):
    try:
        facilities = await FacilitiesService(db).get_facilities()
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return facilities


@router.post("", summary="Создать удобство или услугу")
async def create_facility(
    db: DBDep,
    facilities_data: FacilityAdd = Body(
        openapi_examples={
            "1": {"summary": "Wifi", "value": {"title": "Wifi"}},
            "2": {"summary": "Parking", "value": {"title": "Parking"}},
            "3": {"summary": "Balcony", "value": {"title": "Balcony"}},
            "4": {"summary": "Conditioner", "value": {"title": "Conditioner"}},
        }
    ),
):
    try:
        facilities = await FacilitiesService(db).create_facility(facilities_data)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK", "data": facilities}


@router.delete("/{facilities_id}", summary="Удалить удобство или услугу")
async def delete_facility(db: DBDep, facilities_id: int):
    try:
        await FacilitiesService(db).delete_facility(facilities_id)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except FacilitiesNotFoundException as ex:
        raise FacilitiesNotFoundHTTPException from ex
    return {"status": "OK"}
