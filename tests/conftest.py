import json

import pytest

from src.DB import Base, engine_null_pool
from src.config import settings
from src.main import app
from src.models import *
from httpx import AsyncClient, ASGITransport


@pytest.fixture(scope="session", autouse=True)
async def check_test_mode():
    assert settings.MODE == 'TEST'


@pytest.fixture(scope="session", autouse=True)
async def async_main(check_test_mode):
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session", autouse=True)
async def test_create_user(async_main):
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(
            "/auth/register",
            json={
                "email": "cat@mail.com",
                "password": "123456789",
                "first_name": "cat",
                "last_name": "barsic",
            }
        )


@pytest.fixture(scope="session", autouse=True)
async def create_test_hotel(async_main):
    with open("tests/mock_hotels.json", "r", encoding="utf-8") as f:
        hotels = json.load(f)
    for hotel in hotels:
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resource = await ac.post(
                "/hotels",
                json=hotel
            )


@pytest.fixture(scope="session", autouse=True)
async def create_test_rooms(create_test_hotel):
    with open("tests/mock_rooms.json", "r", encoding="utf-8") as f:
        rooms = json.load(f)
    for room in rooms:
        hotel_id = room["hotel_id"]
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            resource = await ac.post(
                f"/hotels/{hotel_id}/rooms",
                json=room
            )
            print(resource.json())