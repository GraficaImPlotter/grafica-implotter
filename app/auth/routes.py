from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.auth.utils import verificar_senha, criar_token
from app.auth.models import Usuario
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Página de login (GET)
@router.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

# Processa o login (POST)
@router.post("/login")
async def login(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    form = await request.form()
    email = form.get("email")
    senha = form.get("senha")

    resultado = await db.execute(select(Usuario).where(Usuario.email == email))
    usuario = resultado.scalar_one_or_none()

    if not usuario or not verificar_senha(senha, usuario.senha_hash):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "erro": "Credenciais inválidas"},
            status_code=401,
        )

    # Cria o token JWT
    token = criar_token({"sub": usuario.email})

    # Redireciona para o painel e armazena o token em um cookie
    response = RedirectResponse(url="/painel", status_code=302)
    response.set_cookie(key="token", value=token, httponly=True)
    return response
