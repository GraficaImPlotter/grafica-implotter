from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship
from app.database import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    data = Column(DateTime)
    total = Column(Float)
    forma_pagamento = Column(String)

    # Relacionamento com cliente
    cliente = relationship("Cliente", back_populates="vendas")

from sqlalchemy.orm import relationship
from app.models.item_venda import ItemVenda

    itens = relationship("ItemVenda", back_populates="venda")