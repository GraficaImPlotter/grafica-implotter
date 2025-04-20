from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import importlib

from app.database import engine, Base, get_db
from app.auth.routes import router as auth_router
from app.auth.dependencies import get_usuario_logado
from app.routes.produtos import router as produtos_router
from app.routes.clientes import router as clientes_router
from app.routes.vendas import router as vendas_router
from app.routes.cadastros import router as cadastros_router
from app.initial_data.produtos import inserir_produtos_iniciais

# Cria o app
app = FastAPI()

# Monta arquivos estáticos e público
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

# Configura os templates do Jinja2
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# Habilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rota pública (index)
@app.get("/", response_class=FileResponse := importlib.import_module('fastapi.responses').FileResponse)
async def pagina_principal():
    return FileResponse("public/index.html")

# Inclui rotas
app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(clientes_router)
app.include_router(vendas_router)
app.include_router(cadastros_router)

# Startup: cria tabelas e insere dados iniciais
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    # Inserir produtos iniciais
    async for db in get_db():
        await inserir_produtos_iniciais()