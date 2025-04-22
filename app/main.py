
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.database import engine, Base, get_db
from app.auth.routes import router as auth_router
from app.routes.vendas import router as vendas_router
from app.routes.produtos import router as produtos_router
from app.routes.clientes import router as clientes_router
from app.routes.cadastros import router as cadastros_router

app = FastAPI()

# Static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/public", StaticFiles(directory="public"), name="public")

# Templates
templates = Jinja2Templates(directory="app/templates")
app.state.templates = templates

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Página inicial
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Painel
@app.get("/painel", response_class=HTMLResponse)
async def painel(request: Request, usuario=Depends(get_db)):
    return templates.TemplateResponse("painel.html", {"request": request, "usuario": usuario})

# Rotas
app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(clientes_router)
app.include_router(vendas_router)
app.include_router(cadastros_router)

# Startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
