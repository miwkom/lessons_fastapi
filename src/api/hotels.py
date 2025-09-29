from datetime import date
from typing import Optional

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.exceptions import (
    ObjectNotFoundException,
    RoomNotFoundException,
    DataProcessingErrorsException,
    DataProcessingErrorsHTTPException,
    HotelNotFoundException,
    HotelNotFoundHTTPException,
    DatesAreIncorrectException,
    DatesAreIncorrectHTTPException,
)
from src.schemas.hotels import HotelPATCH, HotelAdd
from src.services.hotels import HotelServices

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
@cache(expire=60)
async def get_hotels(
    db: DBDep,
    pagination: PaginationDep,
    title: Optional[str] = Query(None, description="Название"),
    location: Optional[str] = Query(None, description="Адрес"),
    date_from: date = Query(examples="2025-01-27"),
    date_to: date = Query(examples="2025-03-27"),
):
    try:
        hotels = await HotelServices(db).get_filtered_by_time(
            pagination, title, location, date_from, date_to
        )
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except DatesAreIncorrectException as ex:
        raise DatesAreIncorrectHTTPException from ex
    return hotels


@router.get("/{hotel_id}", summary="Получить отель")
@cache(expire=60)
async def get_hotel(hotel_id: int, db: DBDep):
    try:
        hotel = await HotelServices(db).get_hotel(hotel_id)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    return hotel


@router.post("", summary="Создать отель")
async def create_hotel(
    db: DBDep,
    hotel_data: HotelAdd = Body(
        openapi_examples={
            "1": {
                "summary": "Rich",
                "value": {"title": "Rich", "location": "Москва, ул.Дыбенко, 10"},
            },
            "2": {
                "summary": "Lux",
                "value": {"title": "Lux", "location": "Санкт-Петербург, ул.Речная, 25"},
            },
            "3": {
                "summary": "Motel 5 star",
                "value": {"title": "Motel 5 star", "location": "Сочи, ул.Солнечная, 1"},
            },
            "4": {
                "summary": "Novatel",
                "value": {"title": "Novatel", "location": "Москва, ул.Строителей, 12"},
            },
        }
    ),
):
    try:
        hotel = await HotelServices(db).add_hotel(hotel_data)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменить отель")
async def edit_hotel(db: DBDep, hotel_id: int, hotel_data: HotelAdd):
    try:
        await HotelServices(db).edit_hotel(hotel_id, hotel_data)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение")
async def patch_hotel(db: DBDep, hotel_id: int, hotel_data: HotelPATCH):
    try:
        await HotelServices(db).patch_hotel(hotel_id, hotel_data)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(db: DBDep, hotel_id: int):
    try:
        await HotelServices(db).delete_hotel(hotel_id)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK"}
