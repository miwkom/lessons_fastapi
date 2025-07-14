import pytest
from sqlalchemy import text


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


@pytest.fixture(scope="function")
async def delete_all_booking(db):
    if not hasattr(delete_all_booking, 'done'):
        await db.session.execute(text('TRUNCATE TABLE bookings RESTART IDENTITY CASCADE;'))
        await db.session.commit()
        delete_all_booking.done = True


@pytest.mark.parametrize(
    "room_id, date_from, date_to, status_code, quantity_bookings",
    [
        (1, "2024-01-01", "2025-01-07", 200, 1),
        (1, "2024-01-02", "2025-01-08", 200, 2),
        (1, "2024-01-03", "2025-01-09", 200, 3),
    ])
async def test_add_and_get_my_bookings(
        delete_all_booking,
        room_id, date_from, date_to, status_code, quantity_bookings,
        test_authenticated_ac,
):
    response_add_booking = await test_authenticated_ac.post(
        "/bookings",
        json={
            "room_id": room_id,
            "date_from": date_from,
            "date_to": date_to,
        }
    )
    assert response_add_booking.status_code == status_code

    response_get_bookings = await test_authenticated_ac.get("/bookings/me")
    assert response_get_bookings.status_code == status_code
    if status_code == 200:
        res = response_get_bookings.json()
        assert len(res) == quantity_bookings
