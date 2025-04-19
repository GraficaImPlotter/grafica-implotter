from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.cliente import Cliente
from app.auth.dependencies import get_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/clientes/novo", response_class=HTMLResponse)
async def form_novo_cliente(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("clientes_form.html", {"request": request, "usuario": usuario})

@router.post("/clientes/novo")
async def criar_cliente(
    nome: str = Form(...),
    email: str = Form(None),
    telefone: str = Form(None),
    cpf_cnpj: str = Form(None),
    endereco: str = Form(None),
    db: AsyncSession = Depends(get_db)
):
    novo = Cliente(
        nome=nome,
        email=email,
        telefone=telefone,
        cpf_cnpj=cpf_cnpj,
        endereco=endereco
    )
    db.add(novo)
    await db.commit()
    return RedirectResponse("/painel", status_code=303)
