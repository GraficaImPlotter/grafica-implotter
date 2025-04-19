import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Usa a mesma SECRET_KEY que será usada na validação do token
SECRET_KEY = os.getenv("SECRET_KEY", "segredo-super-seguro")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Criptografia de senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)

def gerar_hash_senha(senha):
    return pwd_context.hash(senha)

def criar_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)