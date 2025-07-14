import pytest


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code",
    [
        (1, "2024-01-01", "2025-01-01", 200),
        (1, "2024-01-01", "2025-01-01", 200),
        (1, "2024-01-01", "2025-01-01", 200),
        (1, "2024-01-01", "2025-01-01", 200),
        (1, "2024-01-01", "2025-01-01", 500),
    ])
async def test_add_booking(
        room_id, date_from, date_to, status_code,
        db, test_authenticated_ac
):
    response = await test_authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response.status_code == status_code
    if status_code == 200:
        res = response.json()
        assert isinstance(response.json(), dict)
        assert "data" in res
