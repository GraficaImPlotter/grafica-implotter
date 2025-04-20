from fastapi import APIRouter, Request, Depends, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.database import get_db
from app.models.produto import Produto
from app.auth.dependencies import get_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Listagem de produtos
@router.get("/produtos", response_class=HTMLResponse)
async def listar_produtos(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    result = await db.execute(select(Produto))
    produtos = result.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})

# Formulário de novo produto
@router.get("/produtos/novo", response_class=HTMLResponse)
async def novo_produto(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("produto_form.html", {"request": request, "produto": None, "usuario": usuario})

# Cadastro de novo produto
@router.post("/produtos/novo")
async def salvar_produto(
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    valor_compra: float = Form(...),
    valor_venda: float = Form(...),
    por_m2: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    produto = Produto(
        nome=nome,
        descricao=descricao,
        valor_compra=valor_compra,
        valor_venda=valor_venda,
        por_m2=por_m2
    )
    db.add(produto)
    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)

# Formulário de edição
@router.get("/produtos/{produto_id}/editar", response_class=HTMLResponse)
async def editar_produto(produto_id: int, request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    result = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = result.scalar_one_or_none()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return templates.TemplateResponse("produto_form.html", {"request": request, "produto": produto, "usuario": usuario})

# Atualização de produto
@router.post("/produtos/{produto_id}/editar")
async def atualizar_produto(
    produto_id: int,
    request: Request,
    nome: str = Form(...),
    descricao: str = Form(...),
    valor_compra: float = Form(...),
    valor_venda: float = Form(...),
    por_m2: bool = Form(False),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    result = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = result.scalar_one_or_none()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")

    produto.nome = nome
    produto.descricao = descricao
    produto.valor_compra = valor_compra
    produto.valor_venda = valor_venda
    produto.por_m2 = por_m2

    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)

# Exclusão de produto
@router.get("/produtos/{produto_id}/excluir")
async def excluir_produto(produto_id: int, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    result = await db.execute(select(Produto).where(Produto.id == produto_id))
    produto = result.scalar_one_or_none()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    
    await db.delete(produto)
    await db.commit()
    return RedirectResponse(url="/produtos", status_code=303)
