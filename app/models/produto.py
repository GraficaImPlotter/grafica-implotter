from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    valor_compra = Column(Float, nullable=True)  # Valor que a gráfica paga
    preco_venda = Column(Float, nullable=True)   # Preço final ao cliente
    unidade = Column(String, nullable=True)      # Ex: un, m², pacote
