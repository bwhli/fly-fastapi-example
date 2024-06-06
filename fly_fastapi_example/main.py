import os
import time

from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory=PROJECT_DIR / "static"),
    name="static",
)


@app.get("/")
async def get_endpoint():
    return JSONResponse(
        content={
            "message": f'Hello from {os.getenv("FLY_ALLOC_ID")}!',
        },
    )


@app.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await websocket.accept()
    while True:
        await websocket.send_text(f"Current Timestamp: {int(time.time())}")
        time.sleep(1)
