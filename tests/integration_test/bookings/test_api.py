import pytest
from tests.conftest import get_db_null_pool


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
        test_authenticated_ac
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


@pytest.fixture(scope="module")
async def delete_all_booking():
    async for _db in get_db_null_pool():
        await _db.bookings.delete()
        await _db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, quantity_bookings",
    [
        (1, "2024-01-01", "2025-01-07", 1),
        (1, "2024-01-02", "2025-01-08", 2),
        (1, "2024-01-03", "2025-01-09", 3),
    ])
async def test_add_and_get_my_bookings(
        room_id,
        date_from,
        date_to,
        quantity_bookings,
        test_authenticated_ac,
        delete_all_booking,
):
    response_add_booking = await test_authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response_add_booking.status_code == 200

    response_get_bookings = await test_authenticated_ac.get("/bookings/me")
    assert response_get_bookings.status_code == 200
    assert len(response_get_bookings.json()) == quantity_bookings
