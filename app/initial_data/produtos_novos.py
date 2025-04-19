from sqlalchemy.future import select
from app.models.produto import Produto
from app.database import get_db

FRETE_FIXO = 9.90
LUCRO_PERCENTUAL = 0.65

produtos_novos = [
    {"nome": "ABRIDORES E CHAVEIROS - GRAVAÇÃO A LASER", "descricao": "ABRIDORES E CHAVEIROS", "custo": 28.50, "por_m2": False},
    {"nome": "ADESIVO VINIL FOSCO (1x0)", "descricao": "ADESIVO VINIL FOSCO", "custo": 37.90, "por_m2": True},
    {"nome": "ADESIVO VINIL BRILHO (1x0)", "descricao": "ADESIVO VINIL BRILHO", "custo": 37.90, "por_m2": True},
    {"nome": "ADESIVO VINIL TRANSPARENTE", "descricao": "ADESIVO TRANSPARENTE", "custo": 48.90, "por_m2": True},
    {"nome": "ADESIVO VINIL JATEADO", "descricao": "ADESIVO VINIL JATEADO", "custo": 53.90, "por_m2": True},
    {"nome": "ADESIVO VINIL REFLETIVO", "descricao": "ADESIVO VINIL REFLETIVO", "custo": 89.90, "por_m2": True},
    {"nome": "ADESIVO VINIL PERFURADO", "descricao": "ADESIVO VINIL PERFURADO", "custo": 89.90, "por_m2": True},
    {"nome": "ADESIVO VINIL OURO/PRATA", "descricao": "ADESIVO VINIL OURO/PRATA", "custo": 69.90, "por_m2": True},
    {"nome": "ADESIVO CORTE ELETRÔNICO", "descricao": "ADESIVO CORTE ELETRÔNICO", "custo": 59.90, "por_m2": True},
]

async def inserir_produtos_novos():
    async for db in get_db():
        for item in produtos_novos:
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
