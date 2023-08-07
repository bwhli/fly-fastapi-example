import os

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def get_root():
    return {
        "message": f'Hello World from {os.getenv("FLY_ALLOC_ID")}!',
    }
