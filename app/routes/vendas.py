from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime

from app.database import get_db
from app.auth.dependencies import get_usuario_logado
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.models.produto import Produto
from app.models.item_venda import ItemVenda
from app.utils.mercadopago import gerar_pix

router = APIRouter()

@router.get("/vendas", response_class=HTMLResponse)
async def listar_vendas(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado), data_inicial: str = None, data_final: str = None):
    query = select(Venda).order_by(Venda.data.desc())

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
        query = query.where(Venda.data >= data_inicial)

    if data_final:
        data_final = datetime.strptime(data_final, "%Y-%m-%d")
        query = query.where(Venda.data <= data_final)

    vendas = (await db.execute(query)).scalars().all()
    return request.app.state.templates.TemplateResponse("vendas.html", {
        "request": request,
        "vendas": vendas,
        "usuario": usuario
    })

@router.get("/vendas/nova")
async def nova_venda(request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    clientes = (await db.execute(select(Cliente))).scalars().all()
    produtos = (await db.execute(select(Produto))).scalars().all()
    return request.app.state.templates.TemplateResponse("venda_form.html", {
        "request": request,
        "usuario": usuario,
        "clientes": clientes,
        "produtos": produtos
    })

@router.post("/vendas/nova")
async def salvar_venda(
    request: Request,
    cliente_id: int = Form(...),
    forma_pagamento: str = Form(...),
    observacao: str = Form(""),
    produto_id: list[int] = Form(...),
    quantidade: list[int] = Form(...),
    db: AsyncSession = Depends(get_db)
):
    nova = Venda(cliente_id=cliente_id, forma_pagamento=forma_pagamento, data=datetime.now())
    db.add(nova)
    await db.commit()
    await db.refresh(nova)

    total = 0
    for pid, qtd in zip(produto_id, quantidade):
        produto = await db.get(Produto, pid)
        subtotal = produto.preco_venda * int(qtd)
        item = ItemVenda(venda_id=nova.id, produto_id=pid, quantidade=qtd, subtotal=subtotal)
        db.add(item)
        total += subtotal

    nova.total = total
    nova.observacao = observacao
    await db.commit()

    # Geração do QR Code Pix
    qr_path = await gerar_pix(total)

    return FileResponse(qr_path, media_type="image/png", filename="pix.png")