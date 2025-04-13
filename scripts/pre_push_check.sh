#!/bin/bash

echo "🔍 Rodando lint (ruff)..."
ruff check .

echo "🧪 Rodando testes com coverage..."
coverage run -m pytest --cov-report=xml
coverage report --fail-under=100

echo "✅ Tudo certo para o push!"
