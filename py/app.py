from fastapi import FastAPI
from settings import Settings

settings = Settings()
app = FastAPI()


@app.get("/")
async def root():
    return dict(message="Ok")


@app.post("/")
async def routine():
    return dict(message="Ok")
    # async with httpx.AsyncClient() as client:
    #     tasks = [client.get("https://api.example.com/data") for _ in range(3)]
    #     responses = await asyncio.gather(*tasks)
    # return [r.json() for r in responses]
