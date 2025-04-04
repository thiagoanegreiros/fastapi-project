import os

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from api.routes import user_router
from core.container import Container
from core.log_utils import RequestLoggingMiddleware

app = FastAPI()

container = Container()
container.init_resources()
app.container = container

# 🧱 Cria o banco se ele ainda não existir
if not os.path.exists("db.sqlite3"):
    print("📦 Criando banco de dados e tabelas...")
    SQLModel.metadata.create_all(container.engine())
    print("✅ Banco criado com sucesso!")
else:
    print("📁 Banco já existe, sem necessidade de criar.")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router.router)
app.add_middleware(RequestLoggingMiddleware)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def read_root():
    return {"message": "Hexagonal Architecture API! "}
