from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from app.auth.dependencies import get_usuario_logado
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

@router.get("/clientes", response_class=HTMLResponse)
async def listar_clientes(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("clientes.html", {"request": request, "usuario": usuario})
