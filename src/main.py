import asyncio
import sys
from contextlib import asynccontextmanager
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import uvicorn
from fastapi import FastAPI

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.api.hotels import router as hotel_router
from src.api.auth import router as auth_router
from src.api.rooms import router as rooms_router
from src.api.bookings import router as bookings_router
from src.api.facilities import router as facilities_router
from src.api.images import router as images_router
from src.init import redis_connector
from src.api.dependencies import get_db


async def send_emails_bookings_today_checkin():
    async for db in get_db():
        bookings = await db.bookings.get_bookings_with_today_checkin()
        print(f"{bookings=}")


async def run_send_emails_regularly():
    while True:
        await send_emails_bookings_today_checkin()
        await asyncio.sleep(5)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Старт
    asyncio.create_task(run_send_emails_regularly())
    await redis_connector.connect()

    FastAPICache.init(RedisBackend(redis_connector.redis), prefix="fastapi-cache")
    print('Redis connection')
    yield
    # Выключение/Перезапуск
    await redis_connector.disconnect()
    print('Redis disconnection')


app = FastAPI(lifespan=lifespan)

app.include_router(auth_router)
app.include_router(hotel_router)
app.include_router(rooms_router)
app.include_router(facilities_router)
app.include_router(bookings_router)
app.include_router(images_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
