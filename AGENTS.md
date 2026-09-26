# AGENTS.md

## Overview

REST API for hardware items (`nome`, `preco`, `em_oferta`). CRUD already works (GET, POST, PUT, DELETE). The next work is security: protect data and keep the server stable if the API is public.

## Stack and environment

- Python 3.13.9
- Virtualenv: `venv/` at the repo root (`source venv/bin/activate`)
- FastAPI, Uvicorn, Pydantic, SQLAlchemy, Alembic
- SQLite (`fastapi1/db.sqlite3`)
- `slowapi` is installed (rate limiting later)
- Run the API from `fastapi1/`: `uvicorn main:app --reload`
- Seed one item: `python seed.py` (from `fastapi1/`)
- Migrations: `alembic upgrade head` (from `fastapi1/`)
- Run tests from `fastapi1/`: `../venv/bin/pytest tests/`

## Folder structure

- `venv/` — local virtualenv (gitignored)
- `fastapi1/` — application code
- `fastapi1/main.py` — FastAPI app, table create, router
- `fastapi1/routes.py` — HTTP endpoints
- `fastapi1/schemas.py` — Pydantic request/response models
- `fastapi1/models.py` — SQLAlchemy `Item` / table `itens`
- `fastapi1/repositories.py` — database queries
- `fastapi1/database.py` — engine, session, `get_db`
- `fastapi1/authentication.py` — API key check for write routes
- `fastapi1/seed.py` — inserts one sample item
- `fastapi1/db.sqlite3` — SQLite file (gitignored)
- `fastapi1/alembic.ini` — Alembic config and DB URL
- `fastapi1/alembic/` — migrations
- `fastapi1/alembic/env.py` — Alembic runtime (loads models)
- `fastapi1/alembic/versions/` — migration scripts

## Conventions

- snake_case for files, folders, functions, objects, and attributes
- File and folder names in English
- Function and object names (and their attributes) in Portuguese (pt-BR)
- No comments
- No extra line breaks in code
- Import only what you use

## Guardrails

- Do not add dependencies without asking first and explaining why
- Do not refactor code unrelated to the current task; keep original lines you do not need to change
- If asked to change the database, create a migration
- If unsure, ask before implementing
- Implement changes incrementally by logical unit, run relevant tests after each important change or tightly coupled group of changes, fix any failures before proceeding, and run the full relevant test suite after all planned work is complete.

