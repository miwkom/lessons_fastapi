from fastapi import FastAPI
import uvicorn
from hotels import router as hotel_router
from sync_async import router as sync_async_router

app = FastAPI()

app.include_router(hotel_router)
app.include_router(sync_async_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
