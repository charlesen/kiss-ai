import secrets
from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app.core.auth import get_current_user, get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/admin/templates")

@router.get("/login", response_class=HTMLResponse, include_in_schema=False)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@router.post("/login", include_in_schema=False)
async def login(
    request: Request, 
    username: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # Exemple simplifié de vérification
    from app.core.security import verify_password
    from app.models.user import User
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse("login.html", {"request": request, "error": "Identifiants invalides"})
    response = RedirectResponse(url="/admin", status_code=302)
    return response

@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, current_user = Depends(get_current_user)):
    return templates.TemplateResponse("dashboard.html", {"request": request, "title": "Dashboard Admin", "user": current_user})

@router.post("/generate_api_key", response_class=JSONResponse)
async def generate_api_key(request: Request, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    new_api_key = secrets.token_hex(16)
    current_user.api_key = new_api_key
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return {"api_key": new_api_key}

@router.get("/logout", include_in_schema=False)
async def logout(request: Request, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    current_user.api_key = None
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return RedirectResponse(url="/admin", status_code=302)