from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer
from jose import jwt, JWTError
import os

SECRET_KEY = os.getenv("SECRET_KEY", "segredo")  # Coloque uma chave segura no .env

def get_usuario_logado(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Não autorizado")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
