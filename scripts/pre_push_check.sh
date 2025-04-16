#!/bin/bash

echo "🔍 Rodando lint (ruff)..."
uv run ruff check .

echo "🧪 Rodando testes com coverage..."
uv run coverage run -m pytest --cov-report=xml
uv run coverage report --fail-under=100

echo "✅ Tudo certo para o push!"
