from sqlalchemy import Column, Integer, String, Float, Boolean
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    valor_compra = Column(Float, nullable=False)
    valor_venda = Column(Float, nullable=False)
    por_m2 = Column(Boolean, default=False)
