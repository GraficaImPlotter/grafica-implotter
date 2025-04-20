from fastapi import HTTPException
from sqlalchemy.orm import joinedload

@router.get("/vendas/{venda_id}/excluir")
async def confirmar_exclusao_venda(venda_id: int, request: Request, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Venda).options(joinedload(Venda.cliente)).where(Venda.id == venda_id)
    )
    venda = result.scalar_one_or_none()

    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    return request.app.state.templates.TemplateResponse("confirmar_exclusao_venda.html", {
        "request": request,
        "venda": venda
    })

@router.post("/vendas/{venda_id}/excluir")
async def excluir_venda(venda_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Venda).where(Venda.id == venda_id))
    venda = result.scalar_one_or_none()

    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    await db.execute(delete(ItemVenda).where(ItemVenda.venda_id == venda.id))
    await db.delete(venda)
    await db.commit()

    return RedirectResponse(url="/vendas", status_code=303)
