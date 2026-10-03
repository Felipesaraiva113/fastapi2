# Hardware Items API

![Maintained](https://img.shields.io/badge/Maintained%3F-yes-green.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13-3776AB.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.141-009688.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Neon-4169E1.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

## Descrição

**O que faz:** API RESTful para gestão de itens de hardware (`nome`, `preco`, `em_oferta`) com CRUD completo, autenticação por API key nas rotas de escrita e proteções de produção (rate limiting, CORS, TrustedHost, docs protegidos).

**Construído com:** Python 3.13, FastAPI + Uvicorn, Pydantic v2, SQLAlchemy 2.0 + Alembic, SQLite (dev/teste) / PostgreSQL no Neon (prod), slowapi (rate limiting), python-dotenv, pytest + httpx.

**Por que foi criado:** projeto de estudo e portfólio para consolidar backend (arquitetura em camadas, validação com Pydantic, versionamento de banco com Alembic) e hardening de API pública (menor privilégio, estabilidade sob abuso e deploy Render + Neon).

**Link no ar:** `https://harware-api-1fdc.onrender.com` (troque pela URL real do Render; em prod a documentação interativa fica desligada por segurança).

## Instalação

### Pré-requisitos

- **Git** (qualquer versão recente)
- **Python 3.13+** — confira com `python3 --version`
- **venv** (acompanha o Python) — o projeto usa `venv/` na raiz

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/Felipesaraiva113/fastapi2.git

# 2. Entre na pasta do projeto
cd fastapi2

# 3. Crie e ative o virtualenv, instale as dependências
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Preencha ao menos API_KEY no .env (exigida pelos testes e pelas rotas de escrita)

# 5. Suba o schema com as migrações (a partir de fastapi1/)
cd fastapi1
../venv/bin/alembic upgrade head

# 6. (Opcional, só local) insere um item de exemplo — exige SEED_ENABLED=true no .env
python seed.py
```

## Uso

```bash
# Servidor de desenvolvimento (com reload) — a partir de fastapi1/
uvicorn main:app --reload

# Rodar a suíte de testes (43 testes) — a partir de fastapi1/
../venv/bin/pytest tests/
```

Após iniciar, a API estará acessível em `http://localhost:8000`. A documentação interativa (`/docs` e `/openapi.json`) só existe com `DOCS_ENABLED=true` (dev) e exige a `X-API-Key`; em prod ela é desligada (`404`).

### Autenticação

Leituras (`GET`) são públicas. Escritas (`POST`, `PUT`, `DELETE`) exigem o header `X-API-Key` com o valor da variável `API_KEY`:

| Situação | Resposta |
|---|---|
| Sem header | `401 Chave de API não fornecida` |
| Chave errada | `403 Chave de API inválida` |
| Chave correta | acesso liberado |

### Rate limiting (por IP)

| Rota | Limite |
|---|---|
| `GET /`, `GET /itens/`, `GET /itens/{id}` | `100/min` |
| `POST`, `PUT`, `DELETE` | `10/min` |
| `/docs`, `/openapi.json` | `5/min` |

Acima do limite a API responde `429`.

### Variáveis de ambiente

| Variável | Dev | Prod (Render) |
|---|---|---|
| `DATABASE_URL` | `sqlite:///db.sqlite3` | string pooled do Neon (`?sslmode=require`) |
| `ENVIRONMENT` | `dev` | `prod` |
| `API_KEY` | chave local | chave longa só do servidor |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | origem do frontend (vazio até existir) |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | host do Render (`sua-api.onrender.com`) |
| `DOCS_ENABLED` | `true` | `false` |
| `LOG_LEVEL` | `INFO` | `WARNING` |
| `SEED_ENABLED` | `true` | `false` |

Em `prod` o `create_all` é desligado (fonte única: `alembic upgrade head`) e erros internos retornam `500` genérico sem stack trace. Segredos ficam só no painel do Render — nunca commitados (`.env` e `db.sqlite3` são gitignorados).

### Endpoints (Rotas da API)

#### 1. Listar itens (público, paginado)

##### `GET /itens/?limite=20&deslocamento=0`
Lista itens com paginação (`limite` 1–100, `deslocamento` >= 0).

* **Response (`200 OK`):**
```json
[
  { "id": 1, "nome": "SSD 1TB", "preco": 500.0, "em_oferta": true }
]
```

#### 2. Buscar item por id (público)

##### `GET /itens/{id}`
Retorna um item (`id` > 0) ou `404 Item não encontrado`.

#### 3. Criar item (requer `X-API-Key`)

##### `POST /itens/`
* **Request Body:**
```json
{
  "nome": "SSD 1TB",
  "preco": 500,
  "em_oferta": true
}
```
`nome` obrigatório (1–100 chars), `preco` obrigatório (> 0), `em_oferta` opcional (default `false`). Campos extras são rejeitados (`422`).

* **Response (`201 Created`):**
```json
{ "id": 1, "nome": "SSD 1TB", "preco": 500.0, "em_oferta": true }
```

#### 4. Atualizar item (requer `X-API-Key`)

##### `PUT /itens/{id}`
Aceita atualização parcial (mesmas regras de validação; `null` rejeitado). Inexistente retorna `404`.

* **Request Body:**
```json
{ "preco": 350 }
```

#### 5. Remover item (requer `X-API-Key`)

##### `DELETE /itens/{id}`
Inexistente retorna `404`. Sucesso retorna `204 No Content` (sem corpo).

## Licença

Este projeto é distribuído sob a **licença MIT** — veja o arquivo [LICENSE](./LICENSE) para detalhes. Em resumo: uso comercial, educacional e modificação são permitidos, desde que o aviso de copyright seja mantido.

## Contribuição

### Fluxo de trabalho (GitHub Flow)

1. Atualize a `main`: `git checkout main && git pull`
2. Crie uma branch a partir da `main` com prefixo por tipo:
   - `feature/nome-da-funcionalidade` — funcionalidade nova
   - `fix/descricao-do-ajuste` — correção de bug
   - `docs/o-que-mudou` — documentação
3. Commite em passos pequenos e abra um **Pull Request para a `main`**.
4. Antes de abrir o PR, garanta verde a partir de `fastapi1/`: `../venv/bin/pytest tests/`.
5. Mudança de banco exige migração Alembic (`alembic revision --autogenerate`), nunca edição manual em prod.

### Padrão de commits (Conventional Commits)

```
feat: adiciona paginação em GET /itens/
fix: corrige normalização da URL postgres no env do Alembic
docs: documenta variáveis de ambiente de produção
test: cobre rate limit de DELETE
```

### Conduta

- Testes pytest são obrigatórios em novas rotas.
- Mantenha variáveis sensíveis fora do código (sempre no `.env`, nunca commitado).
- Sem dependência nova sem aprovação prévia.
- Critique o código com respeito nas revisões de PR.

## Owner

| Papel | Responsável | Contato |
|---|---|---|
| Owner / mantenedor | [Felipesaraiva113](https://github.com/Felipesaraiva113) | via [Issues](https://github.com/Felipesaraiva113/fastapi2/issues) do repositório |

Dúvidas, bugs e sugestões: abra uma Issue. Contribuições externas são bem-vindas via Pull Request seguindo o fluxo acima.
