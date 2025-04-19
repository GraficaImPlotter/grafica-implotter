from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)  # ✅ Adicionado
    preco = Column(Float, nullable=False)
    unidade = Column(String, nullable=False)
