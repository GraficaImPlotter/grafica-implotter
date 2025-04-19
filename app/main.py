from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.database import engine, Base
from app.auth.routes import router as auth_router
from app.auth.dependencies import get_usuario_logado
from sqlalchemy.future import select
from app.auth.models import Usuario
from app.auth.utils import gerar_hash_senha
from app.database import get_db

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

# Cria tabelas e usuário admin automaticamente no startup
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Cria usuário admin se ainda não existir
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