from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime

from app.database import get_db
from app.models import Venda, Cliente, Produto, ItemVenda

router = APIRouter()

@router.get("/vendas")
async def listar_vendas(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Venda).order_by(Venda.data.desc()))
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
    produto_id: list[int] = Form(...),
    quantidade: list[int] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Calcular total
    total = 0
    for pid, qtd in zip(produto_id, quantidade):
        result = await db.execute(select(Produto).where(Produto.id == pid))
        produto = result.scalar_one_or_none()
        if produto:
            total += produto.preco_venda * qtd

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=total
    )
    db.add(nova_venda)
    await db.flush()  # pega o ID da venda

    # Salvar itens da venda
    for pid, qtd in zip(produto_id, quantidade):
        db.add(ItemVenda(venda_id=nova_venda.id, produto_id=pid, quantidade=qtd))

    await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
