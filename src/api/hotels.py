from datetime import date
from typing import Optional

from fastapi import Query, APIRouter, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import PaginationDep, DBDep
from src.schemas.hotels import HotelPATCH, HotelAdd

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
# @cache(expire=60)
async def get_hotels(
        db: DBDep,
        pagination: PaginationDep,
        title: Optional[str] = Query(None, description="Название"),
        location: Optional[str] = Query(None, description="Адрес"),
        date_from: date = Query(examples="2025-01-27"),
        date_to: date = Query(examples="2025-03-27"),

):
    per_page = pagination.per_page or 5
    return await db.hotels.get_filtered_by_time(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=per_page,
        offset=per_page * (pagination.page - 1)
    )


@router.get("/{hotel_id}", summary="Получить отель")
@cache(expire=60)
async def get_hotel(
        hotel_id: int,
        db: DBDep
):
    return await db.hotels.get_one_or_none(id=hotel_id)


@router.post("", summary="Создать отель")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {"summary": "Rich",
                  "value": {
                      "title": "Rich",
                      "location": "Москва, ул.Дыбенко, 10"}
                  },
            "2": {"summary": "Lux",
                  "value": {
                      "title": "Lux",
                      "location": "Санкт-Петербург, ул.Речная, 25"}
                  },
            "3": {"summary": "Motel 5 star",
                  "value": {
                      "title": "Motel 5 star",
                      "location": "Сочи, ул.Солнечная, 1"}
                  },
            "4": {"summary": "Novatel",
                  "value": {
                      "title": "Novatel",
                      "location": "Москва, ул.Строителей, 12"}
                  },
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменить отель")
async def edit_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelAdd
):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение")
async def patch_hotel(
        db: DBDep,
        hotel_id: int,
        hotel_data: HotelPATCH
):
    await db.hotels.edit(hotel_data, id=hotel_id, exclude_unset=True)
    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(
        db: DBDep,
        hotel_id: int
):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}
