from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy import delete
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
    result = await db.execute(select(Venda).options(joinedload(Venda.cliente)))
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
        "produtos": result_produtos.scalars().all(),
        "venda": None
    })

@router.post("/vendas/nova")
async def salvar_venda(
    request: Request,
    cliente_id: int = Form(...),
    forma_pagamento: str = Form(...),
    produto_id: list[int] = Form(...),
    quantidade: list[int] = Form(...),
    desconto: float = Form(0),
    db: AsyncSession = Depends(get_db)
):
    total = 0
    for pid, qtd in zip(produto_id, quantidade):
        result = await db.execute(select(Produto).where(Produto.id == pid))
        produto = result.scalar_one_or_none()
        if produto:
            total += produto.preco_venda * qtd

    total_final = total - desconto

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=total_final
    )
    db.add(nova_venda)
    await db.flush()

    for pid, qtd in zip(produto_id, quantidade):
        db.add(ItemVenda(venda_id=nova_venda.id, produto_id=pid, quantidade=qtd))

    await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)

@router.get("/vendas/{venda_id}/excluir")
async def excluir_venda(venda_id: int, db: AsyncSession = Depends(get_db)):
    await db.execute(delete(ItemVenda).where(ItemVenda.venda_id == venda_id))
    await db.execute(delete(Venda).where(Venda.id == venda_id))
    await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)