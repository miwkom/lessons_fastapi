async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200


async def test_create_facilities(ac):
    facilities_data = {"title": "Wifi"}
    response = await ac.post("/facilities", json=facilities_data)

    assert response.status_code == 200
