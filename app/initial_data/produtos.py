# app/initial_data/produtos.py

from sqlalchemy.future import select
from app.models.produto import Produto
from app.database import get_db

LUCRO = 0.65
FRETE = 9.90

produtos = [
    {"nome": "Cartão de Visita", "valor_compra": 20.00, "por_m2": False},
    {"nome": "Adesivo Vinil", "valor_compra": 30.00, "por_m2": True},
    {"nome": "Lona", "valor_compra": 25.00, "por_m2": True},
    # ... outros produtos ...
]

async def inserir_produtos_iniciais():
    async for db in get_db():
        for item in produtos:
            result = await db.execute(select(Produto).where(Produto.nome == item["nome"]))
            existente = result.scalar_one_or_none()
            if not existente:
                venda = round(item["valor_compra"] * (1 + LUCRO) + FRETE, 2)
                novo = Produto(
                    nome=item["nome"],
                    valor_compra=item["valor_compra"],
                    valor_venda=venda,
                    por_m2=item["por_m2"]
                )
                db.add(novo)
        await db.commit()
