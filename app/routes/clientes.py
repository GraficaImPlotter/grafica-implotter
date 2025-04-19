from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.future import select
from app.database import get_db
from app.models.cliente import Cliente
from app.auth.dependencies import get_usuario_logado
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/clientes", response_class=HTMLResponse)
async def listar_clientes(request: Request, usuario=Depends(get_usuario_logado), db=Depends(get_db)):
    resultado = await db.execute(select(Cliente))
    clientes = resultado.scalars().all()
    return templates.TemplateResponse("clientes.html", {"request": request, "clientes": clientes, "usuario": usuario})