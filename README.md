# Distributed Workflow Engine

A distributed workflow engine built with FastAPI, SQLAlchemy 2.0 (async), and Python 3.12+.

## Features

- **Async API** — FastAPI with app factory pattern and lifespan context manager
- **Authentication** — JWT access/refresh tokens with Argon2 password hashing
- **Workflow CRUD** — Create, read, update, and delete workflows scoped per user
- **Async Database** — SQLAlchemy 2.0 async with PostgreSQL (asyncpg) in production, SQLite (aiosqlite) in tests
- **Observability** — Structured logging with structlog
- **Migrations** — Alembic for database schema management
- **CI/CD** — GitHub Actions with ruff linting, mypy type checking, and pytest

## Project Structure

```
backend/
├── dwf/
│   ├── main.py                  # App factory + lifespan
│   ├── settings.py              # Pydantic Settings (env-based config)
│   ├── api/
│   │   ├── deps.py              # Shared dependencies (get_db, get_current_user)
│   │   └── routers/
│   │       ├── auth.py          # Register, login, refresh
│   │       ├── health.py        # Health check endpoint
│   │       └── workflows.py     # Workflow CRUD endpoints
│   ├── domain/models/
│   │   ├── user.py              # Pydantic schemas for auth
│   │   └── workflow.py          # Pydantic schemas + WorkflowStatus enum
│   ├── infrastructure/database/
│   │   ├── engine.py            # Async engine + session factory
│   │   └── models/
│   │       ├── base.py          # SQLAlchemy DeclarativeBase
│   │       ├── user.py          # User table
│   │       └── workflow.py      # Workflow table
│   └── services/
│       ├── auth_service.py      # Auth logic (register, login, JWT)
│       └── workflow_service.py  # Workflow CRUD logic
├── tests/
│   ├── conftest.py              # Async fixtures (engine, session, client)
│   └── unit/
│       ├── test_auth.py         # 8 auth tests
│       └── test_workflow.py     # 8 workflow tests
├── migration/                   # Alembic migrations
├── Dockerfile
├── requirements.txt
└── pyproject.toml
```

## Getting Started

### Prerequisites

- Python 3.12+
- PostgreSQL (or Neon for serverless)

### Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your DATABASE_URL and JWT_SECRET_KEY
```

### Environment Variables

| Variable | Description | Example |
|---|---|---|
| `DATABASE_URL` | Async database connection string | `postgresql+asyncpg://user:pass@host/db` |
| `JWT_SECRET_KEY` | Secret key for JWT signing | `openssl rand -hex 32` |
| `LOG_LEVEL` | Logging level (default: `info`) | `debug` |

### Run

```bash
uvicorn dwf.main:app --reload
```

API docs available at `http://localhost:8000/docs`.

### Test

```bash
cd backend
pytest tests/ -v
```

### Lint

```bash
ruff check backend/
ruff format --check backend/
```

### Docker

```bash
docker compose build
docker compose up
```

## API Endpoints

| Method | Path | Description | Auth |
|---|---|---|---|
| `GET` | `/health` | Health check | No |
| `POST` | `/auth/register` | Register new user | No |
| `POST` | `/auth/login` | Login, get tokens | No |
| `POST` | `/auth/refresh` | Refresh access token | No |
| `POST` | `/workflows/` | Create workflow | Yes |
| `GET` | `/workflows/` | List user's workflows | Yes |
| `GET` | `/workflows/{id}` | Get workflow by ID | Yes |
| `PUT` | `/workflows/{id}` | Update workflow | Yes |
| `DELETE` | `/workflows/{id}` | Delete workflow | Yes |

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL + asyncpg
- **Auth**: PyJWT + Argon2
- **Validation**: Pydantic v2
- **Config**: pydantic-settings
- **Logging**: structlog
- **Migrations**: Alembic
- **Testing**: pytest + pytest-asyncio + httpx + aiosqlite
- **Linting**: ruff + mypy
- **CI**: GitHub Actions
