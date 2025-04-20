import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from app.models.venda import Venda
from app.models.cliente import Cliente
from sqlalchemy.future import select
from app.utils.mercadopago import gerar_pix

async def gerar_comprovante_pdf(db, venda_id: int):
    venda = (await db.execute(select(Venda).where(Venda.id == venda_id))).scalars().first()
    cliente = (await db.execute(select(Cliente).where(Cliente.id == venda.cliente_id))).scalars().first()

    caminho = f"comprovantes/venda_{venda.id}.pdf"
    os.makedirs("comprovantes", exist_ok=True)
    c = canvas.Canvas(caminho, pagesize=A4)

    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, 800, "GRÁFICA IMPLOTTER")
    c.setFont("Helvetica", 10)
    c.drawString(50, 785, "CNPJ: 42.619.0001/83")
    c.drawString(50, 770, "Rua Diogo Galeão Noronha, 78 - Ipiranga - Teófilo Otoni - MG")
    c.drawString(50, 755, "E-mail: graficaimplotter@gmail.com")
    c.drawString(50, 740, "WhatsApp: (33) 99144-9635")
    c.drawString(50, 725, "Instagram: @grafica.implotter")

    c.drawString(50, 700, f"Cliente: {cliente.nome}")
    c.drawString(50, 685, f"Forma de Pagamento: {venda.forma_pagamento}")
    c.drawString(50, 670, f"Valor Total: R$ {venda.valor_total:.2f}")
    c.drawString(50, 655, f"Observação: {venda.observacao}")

    if venda.forma_pagamento == "avista":
        qr_code = await gerar_pix(valor=venda.valor_total)
        c.drawImage(qr_code, 50, 500, width=200, height=200)
        c.drawString(50, 470, "Escaneie o QR Code para pagamento via PIX.")

    c.save()
    return caminho
