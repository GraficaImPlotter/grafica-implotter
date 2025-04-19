from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.auth.utils import verificar_senha, criar_token
from app.auth.models import Usuario
from fastapi.templating import Jinja2Templates
from sqlalchemy.future import select

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, email: str = Form(...), senha: str = Form(...), db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(Usuario).where(Usuario.email == email))
    usuario = query.scalar_one_or_none()
    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse("login.html", {"request": request, "erro": "Usuário ou senha inválidos"})
    
    token = criar_token({"sub": usuario.email})
    response = RedirectResponse(url="/painel", status_code=303)
    response.set_cookie("access_token", token)
    return response

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login")
    response.delete_cookie("access_token")
    return response
