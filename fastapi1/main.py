# COMANDO DO UVICORN = uvicorn main:app --reload
import os
import logging
from fastapi import FastAPI, Depends, Query, Request
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from database import engine, Base 
from routes import items_router, limiter
from authentication import conferir_chave, esquema_chave
ambiente = os.getenv('ENVIRONMENT', 'dev')
nivel_log = getattr(logging, os.getenv('LOG_LEVEL', 'INFO' if ambiente == 'dev' else 'WARNING').upper(), logging.INFO)
logging.getLogger().setLevel(nivel_log)
if ambiente != 'prod':
    Base.metadata.create_all(bind = engine)
docs_habilitados = os.getenv('DOCS_ENABLED', 'true' if ambiente == 'dev' else 'false').lower() == 'true'
origens_permitidas = [origem.strip() for origem in os.getenv('ALLOWED_ORIGINS', '').split(',') if origem.strip()]
hosts_permitidos = [host.strip() for host in os.getenv('ALLOWED_HOSTS', '').split(',') if host.strip()]
app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None) 
app.include_router(items_router)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_methods=['GET', 'POST', 'PUT', 'DELETE'],
    allow_headers=['X-API-Key', 'Content-Type'],
    allow_credentials=False,
)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=hosts_permitidos)
@app.exception_handler(Exception)
async def erro_interno(request: Request, erro: Exception):
    logging.getLogger(__name__).error('erro interno: %s', erro)
    return JSONResponse(status_code=500, content={'detail': 'Erro interno do servidor'})
@app.get('/') 
@limiter.limit('100/minute')
async def read_root(request: Request):
    return {'olá': 'mundo'} # mensagem temporária
if docs_habilitados:
    @app.get('/docs')
    @limiter.limit('5/minute')
    async def pagina_documentacao(request: Request, chave: str | None = Depends(esquema_chave), api_key: str | None = Query(default=None)):
        chave_efetiva = api_key or chave
        conferir_chave(chave_efetiva)
        url_esquema = '/openapi.json' if not chave_efetiva else f'/openapi.json?api_key={chave_efetiva}'
        return get_swagger_ui_html(openapi_url=url_esquema, title='Documentação')
    @app.get('/openapi.json')
    @limiter.limit('5/minute')
    async def esquema_aberto(request: Request, chave: str | None = Depends(esquema_chave), api_key: str | None = Query(default=None)):
        conferir_chave(api_key or chave)
        return JSONResponse(app.openapi())
