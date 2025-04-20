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

from app.auth.dependencies import get_usuario_logado
from app.utils.mercadopago import gerar_pix
from app.utils.comprovante_generator import gerar_comprovante_imagem

router = APIRouter()

@router.get("/vendas")
async def listar_vendas(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    result = await db.execute(select(Venda).order_by(Venda.data.desc()))
    vendas = result.scalars().all()
    return request.app.state.templates.TemplateResponse("vendas.html", {
        "request": request,
        "vendas": vendas,
        "usuario": usuario
    })

@router.get("/vendas/nova")
async def nova_venda(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    clientes_result = await db.execute(select(Cliente))
    produtos_result = await db.execute(select(Produto))
    return request.app.state.templates.TemplateResponse("venda_form.html", {
        "request": request,
        "clientes": clientes_result.scalars().all(),
        "produtos": produtos_result.scalars().all(),
        "usuario": usuario
    })

@router.post("/vendas/nova")
async def salvar_venda(
    request: Request,
    cliente_id: int = Form(...),
    forma_pagamento: str = Form(...),
    produto_id: list[int] = Form(...),
    quantidade: list[int] = Form(...),
    desconto: float = Form(0),
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado)
):
    total = 0
    itens_da_venda = []

    for pid, qtd in zip(produto_id, quantidade):
        result = await db.execute(select(Produto).where(Produto.id == pid))
        produto = result.scalar_one_or_none()
        if produto:
            valor_item = produto.preco_venda * qtd
            total += valor_item
            itens_da_venda.append({"produto": produto, "quantidade": qtd})

    total_final = total - desconto

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        total=total_final,
        forma_pagamento=forma_pagamento
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

    # Buscar cliente para o comprovante
    cliente_result = await db.execute(select(Cliente).where(Cliente.id == cliente_id))
    cliente = cliente_result.scalar_one_or_none()

    # Gerar comprovante de imagem
    gerar_comprovante_imagem(nova_venda, cliente, itens_da_venda)

    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
