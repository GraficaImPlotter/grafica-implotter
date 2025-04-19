from fastapi import APIRouter, Request, Form, Depends, HTTPException, status
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.auth.models import Usuario
from app.auth.utils import verificar_senha, criar_token
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(request: Request, email: str = Form(...), senha: str = Form(...), db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Usuario).where(Usuario.email == email))
    usuario = resultado.scalar_one_or_none()

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "erro": "E-mail ou senha inválidos"
        })

    # Aqui usamos o ID do usuário, e não o e-mail
    token = criar_token({"sub": str(usuario.id)})

    response = RedirectResponse(url="/painel", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="token", value=token, httponly=True)
    return response
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("token")
    return response