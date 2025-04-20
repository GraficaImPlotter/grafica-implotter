from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String)
    telefone = Column(String)
    cpf_cnpj = Column(String)
    endereco = Column(String)

    # Relacionamento com vendas
    vendas = relationship("Venda", back_populates="cliente")
