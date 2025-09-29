from datetime import date

from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.exceptions import (
    RoomNotFoundException,
    RoomNotFoundHTTPException,
    HotelNotFoundException,
    DataProcessingErrorsException,
    DataProcessingErrorsHTTPException,
    DatesAreIncorrectException,
    DatesAreIncorrectHTTPException,
    HotelNotFoundHTTPException,
)
from src.schemas.rooms import RoomAddRequest, RoomPatchRequest
from src.services.rooms import RoomServices

router = APIRouter(prefix="/hotels", tags=["Номера отеля"])


@router.get("/{hotel_id}/rooms", summary="Список номеров")
@cache(expire=60)
async def get_rooms(
    hotel_id: int,
    db: DBDep,
    date_from: date = Query(examples="2025-01-27"),
    date_to: date = Query(examples="2025-03-27"),
):
    try:
        rooms = await RoomServices(db).get_filtered_by_time(
            hotel_id, date_from, date_to
        )
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except DatesAreIncorrectException as ex:
        raise DatesAreIncorrectHTTPException from ex
    return rooms


@router.get("/{hotel_id}/rooms/{room_id}", summary="Получить номер")
@cache(expire=60)
async def get_room(
    hotel_id: int,
    room_id: int,
    db: DBDep,
):
    try:
        return await RoomServices(db).get_one_with_rels(hotel_id, room_id)
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex


@router.post("/{hotel_id}/rooms", summary="Создать номер")
async def create_room(
    db: DBDep,
    hotel_id: int,
    room_data: RoomAddRequest = Body(
        openapi_examples={
            "1": {
                "summary": "Номер 1",
                "value": {
                    "title": "Номер 1",
                    "description": "Номер на 1-ом этаже",
                    "price": 1000,
                    "quantity": 4,
                    "facilities_ids": [3],
                },
            },
            "2": {
                "summary": "Номер 2",
                "value": {
                    "title": "Номер 2",
                    "description": "Номер на 2-ом этаже",
                    "price": 2000,
                    "quantity": 3,
                    "facilities_ids": [4],
                },
            },
            "3": {
                "summary": "Номер 3",
                "value": {
                    "title": "Номер 3",
                    "description": "Номер на 3-ем этаже",
                    "price": 3000,
                    "quantity": 4,
                    "facilities_ids": [3, 4],
                },
            },
            "4": {
                "summary": "Номер 4",
                "value": {
                    "title": "Номер 4",
                    "description": "Номер на 4-ом этаже",
                    "price": 4000,
                    "quantity": 2,
                    "facilities_ids": [3, 4],
                },
            },
        }
    ),
):
    try:
        room = await RoomServices(db).create_room(hotel_id, room_data)
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    return {"status": "OK", "data": room}


@router.put("/{hotel_id}/rooms/{room_id}", summary="Изменить номер")
async def edit_room(db: DBDep, hotel_id: int, room_id: int, room_data: RoomAddRequest):
    try:
        await RoomServices(db).edit_room(hotel_id, room_id, room_data)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    return {"status": "OK"}


@router.patch("/{hotel_id}/rooms/{room_id}", summary="Частичное изменение")
async def patch_room(
    db: DBDep, hotel_id: int, room_id: int, room_data: RoomPatchRequest
):
    try:
        await RoomServices(db).patch_room(hotel_id, room_id, room_data)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    return {"status": "OK"}


@router.delete("/{hotel_id}/rooms/{room_id}", summary="Удалить номер")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomServices(db).delete_room(hotel_id, room_id)
    except DataProcessingErrorsException as ex:
        raise DataProcessingErrorsHTTPException from ex
    except HotelNotFoundException as ex:
        raise HotelNotFoundHTTPException from ex
    except RoomNotFoundException as ex:
        raise RoomNotFoundHTTPException from ex
    return {"status": "OK"}
