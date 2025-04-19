from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    admin = Column(Boolean, default=False)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
