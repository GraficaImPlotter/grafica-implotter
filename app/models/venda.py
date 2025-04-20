from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Venda(Base):
    __tablename__ = "vendas"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"))
    forma_pagamento = Column(String, nullable=False)  # "avista" ou "prazo"
    valor_total = Column(Float, nullable=False)
    data = Column(DateTime, default=datetime.utcnow)
    observacao = Column(String)
    status = Column(String, default="pendente")  # pendente, pago, cancelado

    cliente = relationship("Cliente", back_populates="vendas")

# Em models/cliente.py adicione isso se ainda não tiver:
# vendas = relationship("Venda", back_populates="cliente")
