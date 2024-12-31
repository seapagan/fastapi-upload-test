from fastapi import FastAPI, File, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Mount static files (e.g., CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload/")
async def analyze_file(request: Request, file: UploadFile = File(...)):
    # Analyze the file (e.g., get its size)
    file_contents = await file.read()
    file_size = len(file_contents)

    # Return the result to the frontend
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "file_size": file_size, "file_name": file.filename},
    )
