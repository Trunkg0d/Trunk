from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@router.get("/resume")
async def resume(request: Request):
    return templates.TemplateResponse("resume.html", {"request": request})

@router.get("/projects")
async def projects(request: Request):
    return templates.TemplateResponse("projects.html", {"request": request})

@router.get("/publications", response_class=HTMLResponse)
async def publications(request: Request):
    return templates.TemplateResponse("publications.html", {"request": request})