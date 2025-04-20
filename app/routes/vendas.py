from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.auth.dependencies import get_usuario_logado
from app.database import get_db
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.pdf.venda_pdf import gerar_comprovante_pdf

from datetime import datetime

router = APIRouter()

@router.get("/vendas")
async def listar_vendas(request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    vendas = (await db.execute(select(Venda))).scalars().all()
    return request.app.state.templates.TemplateResponse("vendas.html", {
        "request": request,
        "usuario": usuario,
        "vendas": vendas
    })

@router.get("/vendas/nova")
async def nova_venda(request: Request, usuario=Depends(get_usuario_logado), db: AsyncSession = Depends(get_db)):
    clientes = (await db.execute(select(Cliente))).scalars().all()
    return request.app.state.templates.TemplateResponse("venda_form.html", {
        "request": request,
        "usuario": usuario,
        "clientes": clientes
    })

@router.post("/vendas/nova")
async def salvar_venda(
    request: Request,
    cliente_id: int = Form(...),
    forma_pagamento: str = Form(...),
    valor_total: float = Form(...),
    observacao: str = Form(""),
    db: AsyncSession = Depends(get_db)
):
    nova = Venda(
        cliente_id=cliente_id,
        forma_pagamento=forma_pagamento,
        valor_total=valor_total,
        observacao=observacao
    )
    db.add(nova)
    await db.commit()
    await db.refresh(nova)

    caminho_pdf = await gerar_comprovante_pdf(db, nova.id)
    return FileResponse(caminho_pdf, media_type='application/pdf', filename=f"comprovante_venda_{nova.id}.pdf")