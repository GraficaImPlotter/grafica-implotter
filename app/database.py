import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Usa a variável DATABASE_URL fornecida pelo Railway
DATABASE_URL = os.getenv("DATABASE_URL")

# Cria o engine com suporte async
engine = create_async_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

# Dependência para usar com FastAPI
async def get_db():
    async with SessionLocal() as session:
        yield session
