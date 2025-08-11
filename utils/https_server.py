# miralens/utils/http_server.py
import uvicorn
from fastapi import FastAPI, WebSocket
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"status": "Mira Lens server running"}

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_bytes()
        # TODO: Pass data to your existing pipeline (video/audio detection)
        # For now just send back a mock response
        await websocket.send_text("Detections: none")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
