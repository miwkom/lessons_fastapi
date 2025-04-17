from fastapi import FastAPI, Query, Body
import uvicorn
from typing import Optional

app = FastAPI()

hotels = [
    {"id":1, "title":"Сочи", "name":"Отель_1"},
    {"id":2, "title":"Анапа", "name":"Отель_2"}
]

@app.get("/hotels")
def get_hotels(
        id: int = Query(None, description="ID"),
        title: str = Query(None, description="Город"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_

@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(embed=True)
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title
    })
    return {"status": "OK"}

@app.put("/hotels/{hotel_id}")
def update_hotel(
        hotel_id: int,
        title: str = Body(embed=True),
        name: str = Body(embed=True)
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            hotel["title"] = title
            hotel["name"] = name
            return hotel


@app.patch("/hotels/{hotel_id}")
def patch_hotel(
        hotel_id: int,
        title: Optional[str] = Body(default=None, embed=True),
        name: Optional[str] = Body(default=None, embed=True)
):
    for hotel in hotels:
        if hotel["id"] == hotel_id:
            if title and title != "string":
                hotel["title"] = title
            if name and name != "string":
                hotel["name"] = name
            return hotel


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)