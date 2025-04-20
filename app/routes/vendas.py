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
    quantidade: list[str] = Form(...),
    largura: list[str] = Form(...),
    altura: list[str] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    total = 0

    for i, pid in enumerate(produto_id):
        result = await db.execute(select(Produto).where(Produto.id == int(pid)))
        produto = result.scalar_one_or_none()

        if not produto:
            continue

        if produto.unidade == "m²":
            try:
                largura_m = float(largura[i])
                altura_m = float(altura[i])
                area = largura_m * altura_m
                total += produto.preco_venda * area
            except:
                pass
        else:
            try:
                qtd = int(quantidade[i])
                total += produto.preco_venda * qtd
            except:
                pass

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=round(total, 2)
    )
    db.add(nova_venda)
    await db.flush()

    for i, pid in enumerate(produto_id):
        qtd_final = 0
        result = await db.execute(select(Produto).where(Produto.id == int(pid)))
        produto = result.scalar_one_or_none()

        if produto.unidade == "m²":
            try:
                qtd_final = float(largura[i]) * float(altura[i])
            except:
                qtd_final = 0
        else:
            try:
                qtd_final = int(quantidade[i])
            except:
                qtd_final = 0

        db.add(ItemVenda(venda_id=nova_venda.id, produto_id=int(pid), quantidade=qtd_final))

    await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
