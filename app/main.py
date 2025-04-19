from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.auth.routes import router as auth_router
from app.auth.dependencies import get_usuario_logado

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)

@app.get("/")
def home():
    return {"mensagem": "Sistema da Gráfica Implotter Online Iniciado"}

@app.get("/painel", response_class=HTMLResponse)
def painel(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("painel.html", {"request": request, "usuario": usuario})
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.auth.routes import router as auth_router
from app.auth.dependencies import get_usuario_logado

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(auth_router)

@app.get("/")
def home():
    return {"mensagem": "Sistema da Gráfica Implotter Online Iniciado"}

@app.get("/painel", response_class=HTMLResponse)
def painel(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("painel.html", {"request": request, "usuario": usuario})
