import os
import secrets
from pathlib import Path
from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from dotenv import load_dotenv
load_dotenv(Path(__file__).resolve().parent.parent / '.env', override=True)
esquema_chave = APIKeyHeader(name='X-API-Key', auto_error=False)
chave_configurada = os.getenv('API_KEY', '')
def conferir_chave(chave_recebida: str | None) -> None:
    if not chave_recebida:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Chave de API não fornecida')
    if not chave_configurada or not secrets.compare_digest(chave_recebida.encode('utf-8'), chave_configurada.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Chave de API inválida')
async def verificar_chave(chave: str | None = Depends(esquema_chave)) -> str:
    conferir_chave(chave)
    return chave
