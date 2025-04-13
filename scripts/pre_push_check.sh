#!/bin/bash

echo "🔍 Rodando lint (ruff)..."
ruff check .

echo "🧪 Rodando testes com coverage..."
coverage run -m pytest
coverage report --fail-under=100
coverage xml

echo "✅ Tudo certo para o push!"
