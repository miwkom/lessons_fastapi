import asyncio
from fastapi import APIRouter
import time

router = APIRouter(prefix="/test", tags=["Синхронное и асинхронный"])


@router.get("/sync/{id}")
def sync_func(id: int):
    start_time = time.time()
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    end_time = time.time()
    print(f"sync. Закончил {id}: {time.time():.2f}, {end_time - start_time:.2f}")


@router.get("/async/{id}")
async def async_func(id: int):
    start_time = time.time()
    print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    end_time = time.time()
    print(f"аsync. Закончил {id}: {time.time():.2f}, {end_time - start_time:.2f}")
