from sqlalchemy import Column, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.database import Base

class ItemVenda(Base):
    __tablename__ = "itens_venda"

    id = Column(Integer, primary_key=True)
    venda_id = Column(Integer, ForeignKey("vendas.id"))
    produto_id = Column(Integer, ForeignKey("produtos.id"))
    quantidade = Column(Integer)
    subtotal = Column(Float)

    venda = relationship("Venda", back_populates="itens")
    produto = relationship("Produto")