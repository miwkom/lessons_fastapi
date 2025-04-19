from fastapi import Query, APIRouter, Body

from schemas.hotels import Hotel, HotelPATCH

router = APIRouter(prefix="/hotels", tags=["Отели"])

hotels = [
    {"id": 1, "title": "Сочи", "name": "sochi"},
    {"id": 2, "title": "Москва", "name": "moscow"},
    {"id": 3, "title": "Ростов-на-Дону", "name": "rostov"},
    {"id": 4, "title": "Калининград", "name": "kaliningrad"},
    {"id": 5, "title": "Санкт-Петербург", "name": "spb"},
    {"id": 6, "title": "Казань", "name": "kazan"},
    {"id": 7, "title": "Краснодар", "name": "krasnodar"},
    {"id": 8, "title": "Новосибирск", "name": "novosibirsk"},
    {"id": 9, "title": "Екатеринбург", "name": "ekaterinburg"},
    {"id": 10, "title": "Нижний Новгород", "name": "nn"},
]


@router.get("", summary="Список отелей")
def get_hotels(
        id: int = Query(None, description="ID"),
        title: str = Query(None, description="Город"),
        page: int | None = Query(1, description="Номер страницы"),
        per_page: int | None = Query(3, description="Количество отелей на странице"),
):
    filtered_hotels = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        filtered_hotels.append(hotel)

    start = (page - 1) * per_page
    end = page * per_page
    paginated_hotels = filtered_hotels[start:end]

    return paginated_hotels


@router.delete("/{hotel_id}", summary="Удалить отель")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@router.post("", summary="Создать отель")
def create_hotel(hotel_data: Hotel = Body(openapi_examples={
    "1": {"summary": "Пример 1", "value": {"title": "Сочи", "name": "Отель_пример_1"}},
    "2": {"summary": "Пример 2", "value": {"title": "Анапа", "name": "Отель_пример_2"}},
    "3": {"summary": "Пример 3", "value": {"title": "Сочи", "name": "Отель_пример_3"}},
    "4": {"summary": "Пример 4", "value": {"title": "Анапа", "name": "Отель_пример_4"}},
})):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": hotel_data.title,
        "name": hotel_data.name,
    })
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
