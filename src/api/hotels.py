from typing import Optional

from fastapi import Query, APIRouter, Body

from src.DB import async_session_maker
from src.api.dependencies import PaginationDep
from src.repositories.hotels import HotelsRepository
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: Optional[str] = Query(None, description="Название"),
        location: Optional[str] = Query(None, description="Адрес"),

):
    per_page = pagination.per_page or 5
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_all(
            title=title,
            location=location,
            limit=per_page,
            offset=per_page * (pagination.page - 1)
        )


@router.get("/{hotel_id}", summary="Получить отель")
async def get_hotel(hotel_id: int):
    async with async_session_maker() as session:
        return await HotelsRepository(session).get_one_or_none(id=hotel_id)


@router.post("", summary="Создать отель")
async def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Rich",
          "value": {
              "title": "Rich",
              "location": "Москва, ул.Дыбенка, 10"}
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
})):
    async with async_session_maker() as session:
        hotel = await HotelsRepository(session).add(hotel_data)
        await session.commit()
    return {"status": "OK", "data": hotel}


@router.put("/{hotel_id}", summary="Изменить отель")
async def edit_hotel(hotel_id: int, hotel_data: Hotel):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение")
async def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    async with async_session_maker() as session:
        await HotelsRepository(session).edit(hotel_data, id=hotel_id, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}", summary="Удалить отель")
async def delete_hotel(hotel_id: int):
    async with async_session_maker() as session:
        await HotelsRepository(session).delete(id=hotel_id)
        await session.commit()
    return {"status": "OK"}
