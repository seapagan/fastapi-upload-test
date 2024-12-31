import json
import os
import re
import time
import uuid

from fastapi import FastAPI, File, Request, UploadFile, WebSocket, WebSocketDisconnect
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files (e.g., CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Directory to save uploaded files
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Maximum file size (100 MB)
MAX_FILE_SIZE = 100_000_000  # 100 MB in bytes


# Sanitize filename and add a unique prefix if necessary
def sanitize_filename(filename: str | None) -> str:
    # Get the current Unix timestamp
    timestamp = int(time.time())

    if filename is None:
        # Generate a unique suffix using UUID
        unique_suffix = uuid.uuid4().hex[:8]  # First 8 characters of a UUID
        return f"{timestamp}_unnamed_file_{unique_suffix}"
    # Replace invalid characters with underscores
    sanitized = re.sub(r"[^\w\.-]", "_", filename)
    # Ensure the filename is not empty
    return (
        f"{timestamp}_{sanitized}"
        if sanitized
        else f"{timestamp}_unnamed_file_{uuid.uuid4().hex[:8]}"
    )


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Store active WebSocket connections
active_connections = {}


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    active_connections[client_id] = websocket
    try:
        while True:
            # Wait for a message from the client (optional)
            data = await websocket.receive_text()
            # Send a confirmation message
            await websocket.send_text(
                json.dumps({"status": "connected", "client_id": client_id})
            )
    except WebSocketDisconnect:
        del active_connections[client_id]
        print(f"Client {client_id} disconnected")


@app.post("/upload/")
async def analyze_file(request: Request, file: UploadFile = File(...)):
    try:
        # Sanitize the filename and ensure it's unique
        safe_filename = sanitize_filename(file.filename)

        # Save the file to disk and enforce size limit
        file_path = os.path.join(UPLOAD_DIR, safe_filename)
        file_size = 0

        with open(file_path, "wb") as buffer:
            while chunk := await file.read(8192):  # Read file in chunks of 8 KB
                file_size += len(chunk)
                if file_size > MAX_FILE_SIZE:
                    # Delete the partially uploaded file
                    os.remove(file_path)
                    raise HTTPException(
                        status_code=413, detail="File size exceeds the 100 MB limit"
                    )
                buffer.write(chunk)

        # Analyze the file (e.g., get its size)
        file_size = os.path.getsize(file_path)

        # Send the file name and size to the frontend via WebSocket
        for connection in active_connections.values():
            await connection.send_text(
                json.dumps(
                    {
                        "file_name": safe_filename,
                        "file_size": file_size,
                    }
                )
            )

        return {"message": "File uploaded successfully."}
    except HTTPException as exc:
        return {"error": exc.detail}
    except Exception as exc:
        return {"error": f"An error occurred while processing the file: {str(exc)}"}
