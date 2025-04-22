from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
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

from app.utils.mercadopago import gerar_pix

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
    clientes = (await db.execute(select(Cliente))).scalars().all()
    produtos = (await db.execute(select(Produto))).scalars().all()
    return request.app.state.templates.TemplateResponse("venda_form.html", {
        "request": request,
        "clientes": clientes,
        "produtos": produtos
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

    # Busca a venda com relacionamento completo
    result = await db.execute(
        select(Venda)
        .options(
            selectinload(Venda.cliente),
            selectinload(Venda.itens).selectinload(ItemVenda.produto)
        )
        .where(Venda.id == nova_venda.id)
    )
    venda_completa = result.scalars().first()

    # Geração do código PIX
    codigo_pix = await gerar_pix(venda_completa.total)

    return request.app.state.templates.TemplateResponse("comprovante.html", {
        "request": request,
        "venda": venda_completa,
        "itens": venda_completa.itens,
        "pix_code": codigo_pix
    })

@router.get("/vendas/{venda_id}/excluir")
async def confirmar_exclusao_venda(venda_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Venda).options(selectinload(Venda.cliente)).where(Venda.id == venda_id))
    venda = result.scalars().first()
    if not venda:
        return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)

    return request.app.state.templates.TemplateResponse("confirmar_exclusao_venda.html", {
        "request": request,
        "venda": venda
    })

@router.post("/vendas/{venda_id}/excluir")
async def excluir_venda(venda_id: int, db: AsyncSession = Depends(get_db)):
    venda = await db.get(Venda, venda_id)
    if venda:
        await db.delete(venda)
        await db.commit()
    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
