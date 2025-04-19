from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.dependencies import get_usuario_logado
from app.database import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/clientes/novo")
async def novo_cliente(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("cliente_form.html", {"request": request, "usuario": usuario})

@router.post("/clientes/novo")
async def salvar_cliente(
    request: Request,
    nome: str = Form(...),
    email: str = Form(...),
    telefone: str = Form(...),
    cpf_cnpj: str = Form(...),
    endereco: str = Form(...),
    db: AsyncSession = Depends(get_db),
):
    cliente = Cliente(nome=nome, email=email, telefone=telefone, cpf_cnpj=cpf_cnpj, endereco=endereco)
    db.add(cliente)
    await db.commit()
    return RedirectResponse(url="/clientes", status_code=303)
