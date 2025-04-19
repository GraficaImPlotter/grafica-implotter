from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.auth.dependencies import get_usuario_logado

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/cadastros", response_class=HTMLResponse)
async def cadastros(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("cadastros.html", {"request": request, "usuario": usuario})
