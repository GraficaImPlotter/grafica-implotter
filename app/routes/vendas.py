from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from starlette.status import HTTP_303_SEE_OTHER
from datetime import datetime

from app.database import get_db
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.item_venda import ItemVenda

from app.utils.comprovante_generator import gerar_comprovante

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
    desconto: float = Form(0),
    produto_id: list[int] = Form(...),
    quantidade: list[float] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    total = 0
    itens_da_venda = []

    for pid, qtd in zip(produto_id, quantidade):
        produto = await db.get(Produto, pid)
        if produto:
            subtotal = produto.preco_venda * qtd
            total += subtotal
            itens_da_venda.append({"produto": produto, "quantidade": qtd})

    total_final = total - desconto

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=total_final
    )
    db.add(nova_venda)
    await db.flush()

    for item in itens_da_venda:
        db.add(ItemVenda(
            venda_id=nova_venda.id,
            produto_id=item["produto"].id,
            quantidade=item["quantidade"]
        ))

    await db.commit()

    cliente = await db.get(Cliente, cliente_id)
    gerar_comprovante(nova_venda.id, nova_venda, cliente, itens_da_venda)

    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
