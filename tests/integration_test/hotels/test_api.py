async def test_get_hotels(ac):
    response = await ac.get(
        "/hotels",
        params={
            "date_from": "2024-01-01",
            "date_to": "2025-01-01",
        },
    )

    assert response.status_code == 200
