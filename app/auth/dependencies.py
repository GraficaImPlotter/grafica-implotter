from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from app.auth.models import Usuario
from app.database import get_db
from sqlalchemy.future import select
import os

SECRET_KEY = os.getenv("SECRET_KEY", "segredo-super-seguro")  # mesmo que usou na geração do token
ALGORITHM = "HS256"

async def get_usuario_logado(request: Request, db=Depends(get_db)):
    token = request.cookies.get("token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token não encontrado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")

        resultado = await db.execute(select(Usuario).where(Usuario.id == int(usuario_id)))
        usuario = resultado.scalar_one_or_none()

        if usuario is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não encontrado")

        return usuario

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
