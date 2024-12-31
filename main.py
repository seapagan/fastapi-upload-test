import os
import re
import uuid

from fastapi import FastAPI, File, Request, UploadFile
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
    if filename is None:
        # Generate a unique suffix using UUID
        unique_suffix = uuid.uuid4().hex[:8]  # First 8 characters of a UUID
        return f"unnamed_file_{unique_suffix}"
    # Replace invalid characters with underscores
    sanitized = re.sub(r"[^\w\.-]", "_", filename)
    # Ensure the filename is not empty
    return sanitized or f"unnamed_file_{uuid.uuid4().hex[:8]}"


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


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

        # Return the result to the frontend
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "file_size": file_size, "file_name": safe_filename},
        )
    except HTTPException as exc:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "error": exc.detail},
        )
    except Exception as exc:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"An error occurred while processing the file: {str(exc)}",
            },
        )
