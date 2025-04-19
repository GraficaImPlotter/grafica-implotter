from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.dependencies import get_usuario_logado
from app.database import get_db
from app.models.produto import Produto

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/produtos")
async def listar_produtos(request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Produto))
    produtos = resultado.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})

@router.get("/produtos/novo")
async def novo_produto(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("produto_form.html", {"request": request, "usuario": usuario, "produto": None})

@router.post("/produtos/novo")
async def salvar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    valor_compra: float = Form(...),
    valor_venda: float = Form(...),
    por_m2: bool = Form(False),
    db: AsyncSession = Depends(get_db),
):
    novo = Produto(nome=nome, descricao=descricao, valor_compra=valor_compra, valor_venda=valor_venda, por_m2=por_m2)
    db.add(novo)
    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)

@router.get("/produtos/editar/{produto_id}")
async def editar_produto(produto_id: int, request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = resultado.scalar_one_or_none()
    return templates.TemplateResponse("produto_form.html", {"request": request, "usuario": usuario, "produto": produto})

@router.post("/produtos/editar/{produto_id}")
async def atualizar_produto(
    produto_id: int,
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    valor_compra: float = Form(...),
    valor_venda: float = Form(...),
    por_m2: bool = Form(False),
    db: AsyncSession = Depends(get_db),
):
    resultado = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = resultado.scalar_one_or_none()
    if produto:
        produto.nome = nome
        produto.descricao = descricao
        produto.valor_compra = valor_compra
        produto.valor_venda = valor_venda
        produto.por_m2 = por_m2
        await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)

@router.get("/produtos/excluir/{produto_id}")
async def excluir_produto(produto_id: int, db: AsyncSession = Depends(get_db)):
    resultado = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = resultado.scalar_one_or_none()
    if produto:
        await db.delete(produto)
        await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)
