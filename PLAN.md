# PLAN.md — Hardening API hardware para Web

## 0. Objetivo e princípios
- Proteger dados e manter servidor estável com API pública, sem brechas.
- Menor privilégio: `GET` público, `POST, PUT, DELETE` exigem `X-API-Key`.
- Respeita stack atual: FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic, SQLite, `slowapi`, `python-dotenv`.
- Respeita convenções: `snake_case`, nomes em pt-BR no código, sem comentários novos, só imports usados, sem refator fora do escopo.
- Sem dependência nova de runtime. Só `pytest + httpx` para testes, já aprovado.

## 1. Auth por API key única
- Criar `fastapi1/authentication.py`: lê `API_KEY` via `python-dotenv` + `os.getenv`, header `X-API-Key` com `fastapi.security.APIKeyHeader`, compara com `secrets.compare_digest`, erro `401` sem chave e `403` chave inválida, sem logar chave.
- Aplicar `Depends(verificar_chave)` só em `criar`, `atualizar`, `deletar_por_id` em `fastapi1/routes.py`. `encontrar_por_id` e `obter_todos` seguem públicos.
- Mesma chave protege docs sob demanda.

## 2. Docs protegidos
- Em `fastapi1/main.py`: em prod `docs_url=None, redoc_url=None, openapi_url=None`.
- Rota custom `/docs` e `/openapi.json` protegidas pela mesma `X-API-Key`, toggle por `DOCS_ENABLED=true|false`. Restart do Uvicorn ao trocar (aprovado).
- Dev: `DOCS_ENABLED=true`. Prod: `false` por padrão.
- Rate docs `5/min` por IP.

## 3. Rate limit com slowapi
- Já instalado `slowapi==0.1.10 + limits`. Adicionar `Limiter`, `SlowAPIMiddleware`, handler `429`.
- Limites por IP: `GET /itens/, GET /itens/{id}` -> `100/min`. `POST, PUT, DELETE` -> `10/min`. Docs -> `5/min`.
- Chave por IP de cliente, respeitando proxy quando houver.

## 4. CORS + TrustedHost — implementado com placeholders via env, valores de prod pendentes
- `fastapi1/main.py`: `CORSMiddleware` só com `ALLOWED_ORIGINS` listada, `allow_methods=[GET,POST,PUT,DELETE]`, `allow_headers=[X-API-Key,Content-Type]`, `allow_credentials=False`.
- `TrustedHostMiddleware` com `ALLOWED_HOSTS`. Dev: `localhost,127.0.0.1`. Prod: a definir.
- Origens prod a definir pelo dono antes do deploy.

## 5. Reforço nos schemas
- `fastapi1/schemas.py`: separar `ItemCriacao` com `nome` obrigatório `min_length=1 max_length=100 str_strip`, `preco` obrigatório `gt=0` sem teto, `em_oferta` default `False`.
- `ItemAtualizacao` parcial para `PUT` com mesmos limites.
- `model_config = ConfigDict(extra='forbid', str_strip_whitespace=True)`.
- `id` path `gt=0`. Alinhar `max_length=100` com `models.py String(100)`.
- `response_model` mantido `ItemResposta`.

## 6. Paginação em GET /itens/
- `fastapi1/routes.py obter_todos`: query `limite=Query(20, ge=1, le=100)`, `deslocamento=Query(0, ge=0)`.
- `fastapi1/repositories.py encontrar_todos`: `limit(limite).offset(deslocamento)`.
- Evita dump completo e DoS.

## 7. Banco, logs e deploy
- Remover `Base.metadata.create_all` de `fastapi1/main.py:5` em prod, fonte única `alembic upgrade head` (aprovado). Dev pode manter ou usar Alembic.
- `DATABASE_URL` mantida como está: `sqlite:///db.sqlite3` em `database.py:4`, `alembic.ini:89`, `env.py` lê `os.getenv` com fallback.
- `seed.py` só local com trava `SEED_ENABLED=true|false`. Nunca em prod.
- Remover `print` de `routes.py:34,39` e `seed.py:8`, handler genérico `500` sem stack trace, `LOG_LEVEL=INFO|WARNING`.
- Prod sem `--reload`, HTTPS no proxy.

## 8. Variáveis de ambiente
- `.env` gitignorado + `.env.example` commitado sem segredo, via `python-dotenv`.
```
DATABASE_URL=sqlite:///db.sqlite3
ENVIRONMENT=dev
API_KEY=
ALLOWED_ORIGINS=http://localhost:3000
ALLOWED_HOSTS=localhost,127.0.0.1
DOCS_ENABLED=true
LOG_LEVEL=INFO
SEED_ENABLED=true
```
- Prod exemplo: `ENVIRONMENT=prod`, `DOCS_ENABLED=false`, `LOG_LEVEL=WARNING`, `SEED_ENABLED=false`, `API_KEY` longa aleatória só no servidor.

## 9. Testes com pytest + httpx
- Instalar `pytest + httpx` (aprovado, únicas novas).
- Cobrir: `GET` público ok, `POST/PUT/DELETE` sem chave `401`, chave errada `403`, `429` após estourar, CORS só origem permitida, docs fechado em prod, paginação `le=100`, validação `extra=forbid`, `nome` vazio e `preco<=0` rejeitados.
- Primeira execução: explicar plano e aguardar aprovação conforme `AGENTS.md`.

## 10. Ordem de execução
1. Env + `authentication.py` + wiring `main.py`.
2. Schemas + paginação + repositories.
3. Rate limit + docs protegidos + CORS/TrustedHost (placeholders via env, valores de prod pendentes).
4. Banco/logs/seed trava + remover prints.
5. Testes + `alembic upgrade head` + `seed` local + `uvicorn`.
