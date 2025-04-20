from sqlalchemy import Column, Integer, String, Float
from app.database import Base

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True)
    nome = Column(String)
    preco_venda = Column(Float)