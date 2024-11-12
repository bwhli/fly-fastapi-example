import os
import time

from fastapi import FastAPI, WebSocket, Request, Response, UploadFile, status
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


@app.post("/upload/")
async def upload_file(
    file: UploadFile,
):
    return {
        "filename": file.filename,
    }


@app.get("/replay/region/{region}/")
async def replay_request(
    request: Request,
    region: str,
):
    if region != os.getenv("FLY_REGION"):
        return Response(
            headers={"fly-replay": f"region={region}"},
            status_code=status.HTTP_204_NO_CONTENT,
        )

    return JSONResponse(
        content={
            "machine_id": os.getenv("FLY_ALLOC_ID"),
            "region": os.getenv("FLY_REGION"),
            "replay_source": request.headers.get("fly-replay-src"),
        },
    )


@app.get("/request/")
async def get_request(
    request: Request,
):
    headers_dict = dict(request.headers)
    return JSONResponse(content={"headers": headers_dict})


@app.websocket("/ws/")
async def websocket_endpoint(
    websocket: WebSocket,
):
    await websocket.accept()
    while True:
        await websocket.send_text(f"Current Timestamp: {int(time.time())}")
        time.sleep(1)
