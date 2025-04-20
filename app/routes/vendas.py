from fastapi import Request, APIRouter, Depends, Form
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from datetime import datetime
from fastapi.templating import Jinja2Templates

from app.database import get_db
from app.auth.dependencies import get_usuario_logado
from app.models.venda import Venda
from app.models.cliente import Cliente
from app.pdf.venda_pdf import gerar_comprovante_pdf
from app.utils.mercadopago import gerar_pix

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/vendas", response_class=HTMLResponse)
async def listar_vendas(
    request: Request,
    db: AsyncSession = Depends(get_db),
    usuario=Depends(get_usuario_logado),
    data_inicial: str = None,
    data_final: str = None
):
    query = select(Venda)

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, "%Y-%m-%d")
        query = query.where(Venda.data >= data_inicial)

    if data_final:
        data_final = datetime.strptime(data_final, "%Y-%m-%d")
        query = query.where(Venda.data <= data_final)

    vendas = (await db.execute(query)).scalars().all()
    return templates.TemplateResponse("vendas.html", {
        "request": request,
        "vendas": vendas,
        "usuario": usuario
    })

@router.get("/vendas/nova")
async def nova_venda(
    request: Request,
    usuario=Depends(get_usuario_logado),
    db: AsyncSession = Depends(get_db)
):
    clientes = (await db.execute(select(Cliente))).scalars().all()
    return templates.TemplateResponse("venda_form.html", {
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
