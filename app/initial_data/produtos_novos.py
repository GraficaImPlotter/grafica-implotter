from sqlalchemy.future import select
from app.models.produto import Produto
from app.database import get_db

LUCRO = 0.65
FRETE = 9.90

produtos_lista = [
    {"nome": "Cartão de Visita Couchê 300g 4x4 1000 unid", "custo": 60.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 300g 4x0 1000 unid", "custo": 54.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 250g 4x4 1000 unid", "custo": 56.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 250g 4x0 1000 unid", "custo": 50.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 250g 4x4 500 unid", "custo": 46.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 250g 4x0 500 unid", "custo": 43.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 300g 4x4 500 unid", "custo": 50.00, "por_m2": False},
    {"nome": "Cartão de Visita Couchê 300g 4x0 500 unid", "custo": 45.00, "por_m2": False},
    {"nome": "Imã 7x10 cm", "custo": 110.00, "por_m2": False},
    {"nome": "Imã 9x5 cm", "custo": 90.00, "por_m2": False},
    {"nome": "Imã 9x5 cm - 500 unid", "custo": 48.00, "por_m2": False},
    {"nome": "Folheto A5 Couchê 90g 4x4 1000 unid", "custo": 80.00, "por_m2": False},
    {"nome": "Folheto A6 Couchê 90g 4x4 1000 unid", "custo": 48.00, "por_m2": False},
    {"nome": "Folheto A5 Couchê 90g 4x0 1000 unid", "custo": 65.00, "por_m2": False},
    {"nome": "Folheto A6 Couchê 90g 4x0 1000 unid", "custo": 42.00, "por_m2": False},
    {"nome": "Adesivo Vinil Brilho", "custo": 35.00, "por_m2": True},
    {"nome": "Adesivo Vinil Fosco", "custo": 35.00, "por_m2": True},
    {"nome": "Lona 440g Brilho", "custo": 32.00, "por_m2": True},
    {"nome": "Lona 440g Fosca", "custo": 34.00, "por_m2": True},
    {"nome": "Lona 280g Fosca", "custo": 25.00, "por_m2": True},
    {"nome": "Banner com Bastão", "custo": 40.00, "por_m2": True},
    {"nome": "Placa PS Adesivada", "custo": 70.00, "por_m2": True},
    {"nome": "Adesivo Perfurado", "custo": 42.00, "por_m2": True},
]

async def inserir_produtos_novos():
    async for db in get_db():
        for item in produtos_lista:
            preco = item["custo"] * (1 + LUCRO) + FRETE
            resultado = await db.execute(select(Produto).where(Produto.nome == item["nome"]))
            existente = resultado.scalar_one_or_none()

            if not existente:
                novo = Produto(
                    nome=item["nome"],
                    valor_compra=item["custo"],
                    valor_venda=round(preco, 2),
                    por_m2=item["por_m2"]
                )
                db.add(novo)
        await db.commit()
