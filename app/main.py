from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import shutil
import os
from app.generator import generate_image  # We'll create this

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate/")
async def generate(request: Request, file: UploadFile = File(...), prompt: str = Form(...)):
    filename = f"uploads/{file.filename}"
    with open(filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result_path = generate_image(filename, prompt)  # core function
    return templates.TemplateResponse("index.html", {
        "request": request,
        "input_image": filename,
        "output_image": result_path
    })
