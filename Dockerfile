FROM python:3.12.2-slim

# Instala curl e utilitários para baixar o uv
RUN apt-get update && apt-get install -y curl && apt-get clean

# Instala o uv (binário)
RUN curl -Ls https://astral.sh/uv/install.sh | bash

# Cria o diretório de trabalho
WORKDIR /app

# Copia arquivos de dependência
COPY pyproject.toml uv.lock ./

# Instala as dependências com uv
RUN ~/.cargo/bin/uv venv --python=/usr/local/bin/python && \
    ~/.cargo/bin/uv pip sync

# Copia o restante do código
COPY . .

# Usa o Python e pacotes do ambiente virtual criado pelo uv
ENV PATH="/app/.venv/bin:$PATH"

# Executa o FastAPI com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
