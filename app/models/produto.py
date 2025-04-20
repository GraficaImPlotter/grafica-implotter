
from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    valor_compra = Column(Float)
    preco_venda = Column(Float)
    unidade = Column(String)  # Novo campo
