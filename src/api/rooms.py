from datetime import date

from fastapi import APIRouter, Body, Query

from src.api.dependencies import DBDep
from src.schemas.facilities import RoomsFacilityAdd
from src.schemas.rooms import RoomAdd, RoomPatch, RoomAddRequest, RoomPatchRequest

router = APIRouter(prefix="/hotels", tags=["Номера отеля"])


@router.get("/{hotel_id}/rooms", summary="Список номеров")
async def get_rooms(
        hotel_id: int,
        db: DBDep,
        date_from: date = Query(example="2025-01-27"),
        date_to: date = Query(example="2025-03-27"),
):
    return await db.rooms.get_filtered_by_time(hotel_id=hotel_id, date_from=date_from, date_to=date_to)


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер")
async def get_room(
        hotel_id: int,
        room_id: int,
        db: DBDep,
):
    return await db.rooms.get_room_or_none(hotel_id=hotel_id, id=room_id)


@router.post("/{hotel_id}/rooms", summary="Создать номер")
async def create_room(
        db: DBDep,
        hotel_id: int,
        room_data: RoomAddRequest = Body(openapi_examples={
            "1": {"summary": "Номер 1",
                  "value": {
                      "title": "Номер 1",
                      "description": "Номер на 1-ом этаже",
                      "price": 1000,
                      "quantity": 4,
                      "facilities_ids": [3],
                  }
                  },
            "2": {"summary": "Номер 2",
                  "value": {
                      "title": "Номер 2",
                      "description": "Номер на 2-ом этаже",
                      "price": 2000,
                      "quantity": 3,
                      "facilities_ids": [4],
                  }
                  },
            "3": {"summary": "Номер 3",
                  "value": {
                      "title": "Номер 3",
                      "description": "Номер на 3-ем этаже",
                      "price": 3000,
                      "quantity": 4,
                      "facilities_ids": [3, 4],
                  }
                  },
            "4": {"summary": "Номер 4",
                  "value": {
                      "title": "Номер 4",
                      "description": "Номер на 4-ом этаже",
                      "price": 4000,
                      "quantity": 2,
                      "facilities_ids": [3, 4],
                  }
                  },
        })
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    room = await db.rooms.add(_room_data)

    room_facilities_data = [RoomsFacilityAdd(room_id=room.id, facility_id=f_id) for f_id in room_data.facilities_ids]
    await db.rooms_facilities.add_bulk(room_facilities_data)
    await db.commit()
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер")
async def edit_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomAddRequest
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edit(_room_data, id=room_id, hotel_id=hotel_id)
    await db.rooms_facilities.edit_facility(room_id, facility_id=room_data.facilities_ids)
    await db.commit()
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение")
async def patch_room(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        room_data: RoomPatchRequest
):
    _room_data = RoomPatch(hotel_id=hotel_id, **room_data.model_dump(exclude_unset=True))
    await db.rooms.edit(_room_data, id=room_id, exclude_unset=True)

    if room_data.facilities_ids:
        await db.rooms_facilities.edit_facility(room_id=room_id, facility_id=room_data.facilities_ids)

    await db.commit()
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(
        db: DBDep,
        hotel_id: int,
        room_id: int
):
    await db.rooms.delete(hotel_id=hotel_id, id=room_id)
    await db.commit()
    return {"status": "OK"}
