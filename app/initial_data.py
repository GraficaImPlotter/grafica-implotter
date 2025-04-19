from sqlalchemy.future import select
from app.models.produto import Produto
from app.database import get_db
import asyncio

LUCRO_PERCENTUAL = 0.50  # 50%
FRETE_FIXO = 9.00

produtos_iniciais = [
    {"nome": "Cartão de Visita", "descricao": "Impresso colorido 4x4", "custo": 20.00, "por_m2": False},
    {"nome": "Adesivo Vinil", "descricao": "Impressão em vinil adesivo", "custo": 30.00, "por_m2": True},
    {"nome": "Lona", "descricao": "Impressão em lona", "custo": 25.00, "por_m2": True},
    {"nome": "Panfleto A5", "descricao": "Panfleto colorido frente e verso", "custo": 15.00, "por_m2": False},
    {"nome": "Banner", "descricao": "Banner personalizado com bastão", "custo": 35.00, "por_m2": True},
]

async def inserir_produtos_iniciais():
    async for db in get_db():
        for item in produtos_iniciais:
            resultado = await db.execute(select(Produto).where(Produto.nome == item["nome"]))
            existente = resultado.scalar_one_or_none()
            if not existente:
                preco_venda = item["custo"] * (1 + LUCRO_PERCENTUAL) + FRETE_FIXO
                novo = Produto(
                    nome=item["nome"],
                    descricao=item["descricao"],
                    valor_compra=item["custo"],
                    valor_venda=round(preco_venda, 2),
                    por_m2=item["por_m2"]
                )
                db.add(novo)
        await db.commit()
