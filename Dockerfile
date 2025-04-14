# Usando uma imagem base oficial do Python 3.12
FROM python:3.12.10-slim

# Definindo o diretório de trabalho
WORKDIR /app

# Copiando arquivos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# FastAPI geralmente roda com Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
