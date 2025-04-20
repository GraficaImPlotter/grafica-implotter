from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from app.database import engine, Base, get_db
from app.auth.routes import router as auth_router
from app.auth.dependencies import get_usuario_logado
from app.routes.produtos import router as produtos_router
from app.routes.clientes import router as clientes_router
from app.routes.vendas import router as vendas_router  # <-- NOVO
from app.auth.models import Usuario
from app.auth.utils import gerar_hash_senha
from app.initial_data.produtos import inserir_produtos_iniciais

from sqlalchemy.future import select

# Templates
templates = Jinja2Templates(directory="app/templates")

# App
app = FastAPI()

# Arquivos estáticos
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Rotas
app.include_router(auth_router)
app.include_router(produtos_router)
app.include_router(clientes_router)
app.include_router(vendas_router)  # <-- NOVO

# Página inicial
@app.get("/")
def home():
    return {"mensagem": "Sistema da Gráfica Implotter Online Iniciado"}

# Painel após login
@app.get("/painel", response_class=HTMLResponse)
async def painel(request: Request, usuario=Depends(get_usuario_logado)):
    return templates.TemplateResponse("painel.html", {"request": request, "usuario": usuario})

# Ao iniciar o app
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async for db in get_db():
        resultado = await db.execute(select(Usuario).where(Usuario.email == "graficaimplotter@gmail.com"))
        existe = resultado.scalar_one_or_none()
        if not existe:
            novo_admin = Usuario(
                nome="Administrador",
                email="graficaimplotter@gmail.com",
                senha_hash=gerar_hash_senha("admin123"),
                admin=True
            )
            db.add(novo_admin)
            await db.commit()

    await inserir_produtos_iniciais()
