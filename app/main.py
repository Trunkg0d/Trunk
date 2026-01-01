from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.routers import pages, blog

app = FastAPI(title="Le Pham Hoang Trung - AI Research Blog")

# Mount static files (CSS/JS/Images)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include Routers
app.include_router(pages.router)
app.include_router(blog.router)

@app.on_event("startup")
async def startup():
    print("AI Research Blog is live!")