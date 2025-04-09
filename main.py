import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel

from api.routes import user_router
from core.container import Container
from core.logger.logger_middleware import RequestLoggingMiddleware

load_dotenv()

app = FastAPI()

container = Container()
container.init_resources()

container.config.logging.app.from_env("APP_NAME", "FASTAPI")
container.config.logging.level.from_env("LOG_LEVEL", "INFO")
container.config.logging.to_console.from_env("LOG_TO_CONSOLE", True)
container.config.logging.rotation_days.from_env("ROTATION_DAYS", 5)
container.config.logging.file.from_env("LOG_FILE", "logs/app.log")
container.wire(modules=["core.logger.logger_middleware", "api.routes.user_router"])

app.container = container

logger = container.logger()

if not os.path.exists("db.sqlite3"):
    logger.info("📦 Criando banco de dados e tabelas...")
    SQLModel.metadata.create_all(container.engine())
    logger.info("✅ Banco criado com sucesso!")
else:
    logger.info("📁 Banco já existe, sem necessidade de criar.")

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(user_router.router)
app.add_middleware(RequestLoggingMiddleware)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def read_root():
    return {"message": "Hexagonal Architecture API! "}
