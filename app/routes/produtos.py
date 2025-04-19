from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.future import select
from app.database import get_db
from app.models.produto import Produto
from app.auth.dependencies import get_usuario_logado
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/produtos", response_class=HTMLResponse)
async def listar_produtos(request: Request, usuario=Depends(get_usuario_logado), db=Depends(get_db)):
    resultado = await db.execute(select(Produto))
    produtos = resultado.scalars().all()
    return templates.TemplateResponse("produtos.html", {"request": request, "produtos": produtos, "usuario": usuario})
