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
- ✅ All external API calls and database operations are now fully **asynchronous (async/await)** for maximum I/O performance

---

## 🧱 Project Structure

```
fastapi-project/
├── adapters/                            # Adapters (entry and exit points)
│   ├── inbound/                         # Inbound adapters (e.g., HTTP, GraphQL)
│   │   ├── auth.py                      # Authentication logic (e.g., OAuth2)
│   │   ├── graphql/                     # GraphQL schema and resolvers
│   │   └── routes/                      # REST route handlers
│   │       ├── login_router.py
│   │       ├── movies_router.py
│   │       └── todo_router.py
│   │
│   └── out/                             # Outbound adapters (infrastructure implementations)
│       ├── api/                         # External API clients
│       │   ├── movies_api_client.py
│       │   └── todo_api_client.py
│       └── database/                    # Database persistence layer
│           ├── base_repository.py
│           ├── models.py
│           └── user_repository.py
│
├── application/                         # Application layer (use cases / services)
│   ├── movie_service.py
│   ├── todo_service.py
│   └── user_service.py
│
├── domain/                              # Domain layer (entities and ports/interfaces)
│   ├── movie.py
│   ├── todo.py
│   ├── user.py
│   ├── movie_api_client_interface.py
│   ├── todo_api_client_interface.py
│   └── user_repository_interface.py
│
├── infrastructure/                      # Technical infrastructure (cross-cutting concerns)
│   ├── logger/                          # Logging and exception handling
│   │   ├── exception_handlers.py        # Global exception handlers
│   │   ├── logger.py                    # Logger configuration
│   │   ├── logger_middleware.py         # Request timing / structured logs
│   │   └── request_context.py           # Request-scoped context (e.g., request_id)
│   └── container.py                     # Dependency injection configuration
│
├── logs/                                # Application log files
├── scripts/                             # Utility scripts (e.g., seeding, testing)
├── static/                              # Static assets (optional)
├── tests/                               # Automated tests (organized per layer)
│   └── adapters/inbound/routes/         # Route handler tests
│
├── .env                                 # Environment variables for local/dev use
├── pyproject.toml                       # Project configuration (dependencies, formatting, linting)
└── README.md                            # Project documentation and onboarding
```
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
