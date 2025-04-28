# 🐍 FastAPI Hexagonal App

![CI](https://github.com/thiagoanegreiros/fastapi-project/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/thiagoanegreiros/fastapi-project/actions/workflows/codeql.yml/badge.svg)
[![Codecov](https://codecov.io/gh/thiagoanegreiros/fastapi-project/branch/main/graph/badge.svg)](https://codecov.io/gh/thiagoanegreiros/fastapi-project)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![License](https://img.shields.io/github/license/thiagoanegreiros/fastapi-project.svg)
![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen.svg)

This project is a backend API built with **Python 3.12** and **FastAPI**, following the principles of **Hexagonal Architecture** (Ports & Adapters), with a focus on **testability, readability, observability, and extensibility**.

It demonstrates **modern Python engineering practices**, including structured logging, 100% test coverage, and clean code separation.

API is running on https://python-studies.onrender.com/docs

GraphQL is running on https://python-studies.onrender.com/graphql

---

## 🚀 Features 

- ✅ **FastAPI** with strong typing
- ✅ Hexagonal Architecture (Domain → Application → Infrastructure)
- ✅ **100% unit test coverage** with `pytest`
- ✅ Structured logging with Request ID and execution time
- ✅ Centralized exception handling
- ✅ Dependency injection using `dependency-injector`
- ✅ Environment configuration with `.env`
- ✅ Ready for CI/CD with `pre-commit`, `ruff`, and `coverage`
- ✅ Google OAuth2 login
- ✅ JWT-based login and authentication for stateless APIs ⭐️
- ✅ GraphQL API integration using Strawberry
- ✅ ⚡ This project uses uv for environment and package management. It is fully compatible with pip and extremely fast.
- ✅ Environment configuration with .env using a custom PyPI package: ta-envy

---

## 🧱 Project Structure

```
project-root/
├── .vscode/                      # VS Code editor settings (optional)
│
├── api/                          # HTTP interface layer (FastAPI)
│   ├── graphql/                  # GraphQL (Strawberry)
│   │   └── resolvers.py          # GraphQL resolvers
│   │   └── schema.py             # GraphQL schema definition
│   └── routes/                   # Route definitions organized by domain context (e.g., todo, user)
│       ├── todo_router.py
│       └── user_router.py
│
├── core/                         # Application core following Hexagonal Architecture
│   ├── application/              # Use cases (application services)
│   ├── domain/                   # Business entities, value objects, and abstract interfaces
│   ├── logger/                   # Structured logging with middleware and request context
│   │   ├── exception_handlers.py # Centralized exception management
│   │   ├── logger.py             # Logger setup
│   │   ├── logger_middleware.py  # Middleware for logging and request timing
│   │   └── request_context.py    # Per-request scoped context (e.g., request_id)
│   ├── auth.py                   # Authentication logic (Google OAuth2, etc.)
│   └── container.py              # Dependency injection container using `dependency-injector`
│
├── infrastructure/              # External systems and adapter implementations
│   ├── api/                      # External API clients (e.g., REST clients)
│   │   └── todo_api_client.py
│   └── database/                 # Persistent repositories and models using SQLModel
│       ├── base_repository.py    # Generic base repository with common CRUD logic
│       ├── models.py             # ORM models mapped to the domain
│       └── user_repository.py    # User-specific repository implementation
│
├── logs/                         # Log output files (runtime logs, if enabled)
├── scripts/                      # Utility scripts (e.g., manual testing, data generation)
├── static/                       # Static assets (optional, if needed)
├── tests/                        # Unit tests organized by layer (100% coverage with mocks)
│
├── .env                          # Optional local environment file (loaded via `ta-envy` from PyPI)
├── pyproject.toml                # Project configuration (dependencies, linting, formatting, etc.)
├── README.md                     # Project documentation and usage instructions
└── pre-commit-config.yaml        # Pre-commit hooks (e.g., `ruff`, `black`, `isort`, `coverage`)
```

> All requests go through the API → Application → Infrastructure. Domain layer does not depend on external details.

---

## 🧪 Running Tests

```bash
# Run all tests
uv run coverage run -m pytest --cov-report=xml
```

📈 Test coverage is enforced via a **pre-push hook**.

---

## 🔐 Pre-commit Hooks

Before every commit or push, the project automatically runs:

- `ruff` (lint + autofix)
- `black` (code formatting)
- `pytest` with a minimum coverage threshold (e.g., 90%)

```bash
# Install pre-commit hooks
uv install pre-commit
pre-commit install
```

---

## 📦 Installation

```bash
git clone https://github.com/thiagoanegreiros/fastapi-project
cd fastapi-project
uv venv
source .venv/bin/activate
uv sync
cp .env.example .env
```

---

## ⚙️ Environment Variables

`.env` file example:

```env
APP_ENV=dev
DATABASE_URL=sqlite:///./dev.db
LOG_LEVEL=INFO
```

Loaded automatically via `python-dotenv`.

---

## 📄 Example Log Output

```json
{
  "timestamp": "2025-03-29T14:33:11Z",
  "level": "INFO",
  "request_id": "3e7f4a8c-a73c-4fc3-b16a-68179c3d47d9",
  "method": "POST",
  "path": "/users/",
  "duration_ms": 34,
  "message": "User created successfully"
}
```

> All logs include execution time and unique `request_id`.

---

## ⚠️ Error Handling

- Centralized exception handling with consistent structure
- Stack trace and context are logged at `ERROR` level
- Clean error messages returned to clients

---

## 📬 Main Endpoints

| Method | Route          | Description               |
|--------|----------------|---------------------------|
| GET    | `/users/`      | List all users            |
| POST   | `/users/`      | Create a new user         |
| GET    | `/users/{id}`  | Retrieve user by ID       |
| DELETE | `/users/{id}`  | Delete user by ID         |

---

## 🧠 Purpose

This project serves as a **showcase of advanced Python backend development**, including:

- Clean architecture and modular design
- Full test coverage with mocks
- Dev-friendly tools for formatting and linting
- Logging, observability, and error traceability

---

## 🤝 Contributing

This is a personal project, but contributions and suggestions are welcome!

---

## 🐍 Made by Thiago Ananias
