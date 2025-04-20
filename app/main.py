from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from app.routes.vendas import router as vendas_router
from app.routes.clientes import router as clientes_router
from app.routes.produtos import router as produtos_router
from app.routes.usuarios import router as usuarios_router
from app.database import create_tables
from app.initial_data.produtos import inserir_produtos_iniciais

app = FastAPI()

# Configura os templates do Jinja2
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# Habilita CORS se necessário
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(vendas_router)
app.include_router(clientes_router)
app.include_router(produtos_router)
app.include_router(usuarios_router)

# Cria tabelas e dados iniciais no startup
@app.on_event("startup")
async def on_startup():
    await create_tables()
    await inserir_produtos_iniciais()