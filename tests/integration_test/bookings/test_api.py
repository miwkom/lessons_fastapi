async def test_add_booking(db, test_authenticated_ac):
    room_id = (await db.rooms.get_all())[0].id
    response = await test_authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": "2024-01-01",
            "date_to": "2025-01-01",
        }
    )
    assert response.status_code == 200
    res = response.json()
    assert isinstance(response.json(), dict)
    assert "data" in res