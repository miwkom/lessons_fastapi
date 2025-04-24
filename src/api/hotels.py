from typing import Optional

from fastapi import Query, APIRouter, Body
from sqlalchemy import insert, select

from src.DB import async_session_maker, engine
from src.api.dependencies import PaginationDep
from src.models.hotels import HotelsModel
from src.schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список отелей")
async def get_hotels(
        pagination: PaginationDep,
        title: Optional[str] = Query(None, description="Название"),
        location: Optional[str] = Query(None, description="Адрес"),

):
    per_page = pagination.per_page or 5
    async with (async_session_maker() as session):

        query = select(HotelsModel)
        if title:
            query = query.filter(HotelsModel.title.like(f"%{title}%"))
        if location:
            query = query.filter(HotelsModel.location.like(f"%{location}%"))
        query = (
            query
            .limit(per_page)
            .offset(per_page * (pagination.page - 1))
        )

        result = await session.execute(query)

        hotels = result.scalars().all()
        # print(type(hotels), hotels)
        return hotels
    # if pagination.page and pagination.per_page:
    #     return filtered_hotels[(pagination.page - 1) * pagination.per_page:][:pagination.per_page]


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


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
        add_hotel_stmt = insert(HotelsModel).values(**hotel_data.model_dump())
        # print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await session.execute(add_hotel_stmt)
        await session.commit()
    return {"status": "OK"}


@router.put("/{hotel_id}", summary="Изменить отель")
def edit_hotel(hotel_id: int, hotel_data: Hotel):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    hotel["title"] = hotel_data.title
    hotel["name"] = hotel_data.name
    return {"status": "OK"}


@router.patch("/{hotel_id}", summary="Частичное изменение")
def patch_hotel(hotel_id: int, hotel_data: HotelPATCH):
    global hotels
    hotel = [hotel for hotel in hotels if hotel["id"] == hotel_id][0]
    if hotel_data.title:
        hotel["title"] = hotel_data.title
    if hotel_data.name:
        hotel["name"] = hotel_data.name
    return {"status": "OK"}
