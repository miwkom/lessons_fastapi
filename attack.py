import asyncio
import time
import aiohttp


async def get_data(id: int, route: str):
    print(f"Начал выполнение {id}")
    url = f"http://127.0.0.1:8000/test/{route}/{id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(f"Закончил выполнение {id}")

async def main():
    await asyncio.gather(
        *[get_data(i, "sync") for i in range(500)]
    )

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    total_time = end_time - start_time
    print(f'Общее время работы:{total_time:.2f}')