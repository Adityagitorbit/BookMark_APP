# app/main.py

from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# FastAPI app initialization
app = FastAPI()

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Jinja2 templates directory
templates = Jinja2Templates(directory="templates")


# ---------------------------
# Routes for Serving Templates
# ---------------------------

# Base Page Route
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """
    Serves the base template for common layout.
    """
    return templates.TemplateResponse("base.html", {"request": request})


# Login Page Route
@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serves the login page.
    """
    return templates.TemplateResponse("login.html", {"request": request})


# Dashboard Page Route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_page(request: Request):
    """
    Serves the dashboard page.
    """
    return templates.TemplateResponse("dashboard.html", {"request": request})


# Health Check Route
@app.get("/health")
async def health_check():
    """
    Simple route to check if the server is running.
    """
    return {"status": "Server is running"}
