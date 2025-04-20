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

from app.utils.mercadopago import gerar_pix
from app.utils.comprovante_generator import gerar_comprovante_imagem

router = APIRouter()

@router.get("/vendas")
async def listar_vendas(request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Venda)
        .options(
            selectinload(Venda.cliente),
            selectinload(Venda.itens).selectinload(ItemVenda.produto)
        )
        .order_by(Venda.data.desc())
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
    desconto: float = Form(0),
    produto_id: list[int] = Form(...),
    quantidade: list[float] = Form(...),
    largura: list[float] = Form(...),
    altura: list[float] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    total = 0
    for i in range(len(produto_id)):
        result = await db.execute(select(Produto).where(Produto.id == produto_id[i]))
        produto = result.scalar_one_or_none()
        if produto:
            if produto.unidade == "m²":
                m2 = (largura[i] * altura[i]) / 10000
                total += produto.preco_venda * m2
            else:
                total += produto.preco_venda * quantidade[i]

    total_com_desconto = total - desconto

    nova_venda = Venda(
        cliente_id=cliente_id,
        data=datetime.now(),
        forma_pagamento=forma_pagamento,
        total=total_com_desconto
    )
    db.add(nova_venda)
    await db.flush()

    for i in range(len(produto_id)):
        qtd = quantidade[i]
        result = await db.execute(select(Produto).where(Produto.id == produto_id[i]))
        produto = result.scalar_one_or_none()
        if produto:
            if produto.unidade == "m²":
                qtd = (largura[i] * altura[i]) / 10000
            db.add(ItemVenda(venda_id=nova_venda.id, produto_id=produto_id[i], quantidade=qtd))

    await db.commit()

    # Gerar PIX e comprovante
    payload = {
        "transaction_amount": float(total_com_desconto),
        "description": f"Venda #{nova_venda.id} na Gráfica Implotter",
        "payer_email": "seu-email@exemplo.com",
        "payer_name": "Cliente",
    }
    pix = gerar_pix(payload)
    gerar_comprovante(nova_venda.id, total_com_desconto, forma_pagamento)

    return RedirectResponse("/vendas", status_code=HTTP_303_SEE_OTHER)
