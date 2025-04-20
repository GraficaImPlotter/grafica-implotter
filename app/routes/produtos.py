from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database import get_db
from app.models.produto import Produto
from starlette.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.auth.dependencies import get_usuario_logado  # autenticação

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()

@router.get("/produtos")
async def listar_produtos(request: Request, db: AsyncSession = Depends(get_db), usuario=Depends(get_usuario_logado)):
    result = await db.execute(select(Produto))  # <- CORRIGIDO
    produtos = result.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})
