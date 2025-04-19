from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.auth.dependencies import get_usuario_logado
from app.models.produto import Produto
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/produtos", response_class=HTMLResponse)
async def listar_produtos(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    resultado = await db.execute(select(Produto))
    produtos = resultado.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})

@router.post("/produtos")
async def adicionar_produto(
    nome: str = Form(...),
    descricao: str = Form(""),
    preco_compra: float = Form(...),
    preco_venda: float = Form(...),
    unidade: str = Form("un"),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    novo = Produto(nome=nome, descricao=descricao, preco_compra=preco_compra, preco_venda=preco_venda, unidade=unidade)
    db.add(novo)
    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)
