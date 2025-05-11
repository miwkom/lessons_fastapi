from fastapi import APIRouter, Body

from src.DB import async_session_maker
from src.repositories.rooms import RoomsRepository
from src.schemas.rooms import RoomAdd, RoomPATCH

router = APIRouter(prefix="/hotels", tags=["Номера отеля"])


@router.get("/{hotel_id}/rooms", summary="Список номеров")
async def get_rooms(
        hotel_id: int
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_all(hotel_id)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер")
async def get_room(
        hotel_id: int,
        room_id: int,
):
    async with async_session_maker() as session:
        return await RoomsRepository(session).get_one_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/create_room", summary="Создать номер")
async def create_room(room_data: RoomAdd = Body(openapi_examples={
    "1": {"summary": "Номер 1",
          "value": {
              "hotel_id": 30,
              "title": "Номер 1",
              "description": "Номер на 1-ом этаже",
              "price": 1000,
              "quantity": 4,
          }
          },
    "2": {"summary": "Номер 2",
          "value": {
              "hotel_id": 30,
              "title": "Номер 2",
              "description": "Номер на 2-ом этаже",
              "price": 2000,
              "quantity": 3,
          }
          },
    "3": {"summary": "Номер 3",
          "value": {
              "hotel_id": 30,
              "title": "Номер 3",
              "description": "Номер на 3-ем этаже",
              "price": 3000,
              "quantity": 4,
          }
          },
    "4": {"summary": "Номер 4",
          "value": {
              "hotel_id": 30,
              "title": "Номер 4",
              "description": "Номер на 4-ом этаже",
              "price": 4000,
              "quantity": 2,
          }
          },
})):
    async with async_session_maker() as session:
        room = await RoomsRepository(session).add(room_data)
        await session.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер")
async def edit_room(hotel_id: int, room_id: int, room_data: RoomAdd):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение")
async def patch_room(hotel_id: int, room_id: int, room_data: RoomPATCH):
    async with async_session_maker() as session:
        await RoomsRepository(session).edit(room_data, hotel_id=hotel_id, id=room_id, exclude_unset=True)
        await session.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomsRepository(session).delete(hotel_id=hotel_id, id=room_id)
        await session.commit()
    return {"status": "OK"}
