from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.auth.dependencies import get_usuario_logado
from fastapi.templating import Jinja2Templates
from app.models.produto import Produto

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/produtos", response_class=HTMLResponse)
async def listar_produtos(request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Produto))
    produtos = result.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})

@router.post("/produtos")
async def criar_produto(
    nome: str = Form(...),
    preco: float = Form(...),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    novo_produto = Produto(nome=nome, preco=preco)
    db.add(novo_produto)
    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)
