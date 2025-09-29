async def test_get_facilities(ac):
    response = await ac.get("/facilities")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


async def test_create_facilities(ac):
    facilities_title = "Wifi"
    response = await ac.post("/facilities", json={"title": facilities_title})
    res = response.json()
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "data" in res
    assert res["data"]["title"] == facilities_title
