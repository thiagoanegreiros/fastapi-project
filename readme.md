# 🐍 FastAPI Hexagonal App

![CI](https://github.com/thiagoanegreiros/fastapi-project/actions/workflows/ci.yml/badge.svg)
![CodeQL](https://github.com/thiagoanegreiros/fastapi-project/actions/workflows/codeql.yml/badge.svg)
[![Codecov](https://codecov.io/gh/thiagoanegreiros/fastapi-project/branch/main/graph/badge.svg)](https://codecov.io/gh/thiagoanegreiros/fastapi-project)

This project is a backend API built with **Python 3.12** and **FastAPI**, following the principles of **Hexagonal Architecture** (Ports & Adapters), with a focus on **testability, readability, observability, and extensibility**.

It demonstrates **modern Python engineering practices**, including structured logging, 100% test coverage, and clean code separation.

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
- ✅ Google OAuth2 login with session-based authentication


---

## 🧱 Project Structure

```
core/
├── domain/            # Entities and contracts (pure models)
├── application/       # Use cases (services)
├── container.py       # Dependency Injection setup

infrastructure/
├── database/          # Concrete repositories (SQLModel)

api/
├── routes/            # FastAPI routes connected to the Application layer

tests/
├──                    # Unit tests with mocks and 100% coverage
```

> All requests go through the API → Application → Infrastructure. Domain layer does not depend on external details.

---

## 🧪 Running Tests

```bash
# Run all tests
PYTHONPATH=. pytest --cov

# Show test coverage
coverage report -m
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
pip install pre-commit
pre-commit install
```

---

## 📦 Installation

```bash
git clone https://github.com/thiagoanegreiros/fastapi-project
cd fastapi-project
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
