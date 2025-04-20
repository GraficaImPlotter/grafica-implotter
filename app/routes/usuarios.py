from fastapi import APIRouter

router = APIRouter()

@router.get("/usuarios/teste")
async def teste_usuario():
    return {"mensagem": "Usuário funcionando!"}
