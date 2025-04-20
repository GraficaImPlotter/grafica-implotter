from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime

from app.database import get_db
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.item_venda import ItemVenda

router = APIRouter()

@router.get("/vendas")
async def listar_vendas(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Venda).options(selectinload(Venda.cliente)).order_by(Venda.data.desc())
    )
    vendas = result.scalars().all()
    return request.app.state.templates.TemplateResponse("vendas.html", {
        "request": request,
        "vendas": vendas
    })

@router.get("/vendas/nova")
async def nova_venda(request: Request, db: AsyncSession = Depends(get_db)):
    result_clientes = await db.execute(select(Cliente))
    result_produtos = await db.execute(select(Produto))
    return request.app.state.templates.TemplateResponse("venda_form.html", {
        "request": request,
        "clientes": result_clientes.scalars().all(),
        "produtos": result_produtos.scalars().all()
    })

@router.post("/vendas/nova")
async def salvar_venda(
    request: Request,
    cliente_id: int = Form(...),
    forma_pagamento: str = Form(...),
    desconto: float = Form(0.0),
    produto_id: list[int] = Form(...),
    quantidade: list[int] = Form(...),
    largura: list[float] = Form(None),
    altura: list[float] = Form(None),
    db: AsyncSession = Depends(get_db)
):
    total = 0
    for i, (pid, qtd) in enumerate(zip(produto_id, quantidade)):
        result = await db.execute(select(Produto).where(Produto.id == pid))
        produto = result.scalar_one_or_none()
        if produto:
            if produto.unidade == "m²" and largura and altura and largura[i] and altura[i]:
                area = (largura[i] * altura[i]) / 10000  # converte cm² para m²
                total += produto.preco_venda * area
                qtd = area  # registra a metragem
            else:
                total += produto.preco_venda * qtd

    total_com_desconto = total - desconto

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=total_com_desconto
    )
    db.add(nova_venda)
    await db.flush()  # pega o ID da venda

    for i, (pid, qtd) in enumerate(zip(produto_id, quantidade)):
        if largura and altura and largura[i] and altura[i]:
            result = await db.execute(select(Produto).where(Produto.id == pid))
            produto = result.scalar_one_or_none()
            if produto and produto.unidade == "m²":
                qtd = (largura[i] * altura[i]) / 10000
        db.add(ItemVenda(venda_id=nova_venda.id, produto_id=pid, quantidade=qtd))

    await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
