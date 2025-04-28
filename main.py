import os
from datetime import timedelta

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from strawberry.fastapi import GraphQLRouter
from ta_envy import Env

from api.graphql.schema import schema
from api.routes import todo_router, user_router
from core.auth import create_access_token, verify_access_token
from core.container import Container
from core.logger.exception_handlers import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)
from core.logger.logger_middleware import RequestLoggingMiddleware

env = Env(
    required=[
        "GOOGLE_CLIENT_ID",
        "GOOGLE_CLIENT_SECRET",
        "JWT_SECRET_KEY",
        "REDIRECT_URI",
        "FRONT_REDIRECT_URI",
    ]
)

app = FastAPI()

container = Container()
container.init_resources()

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

container.config.logging.app.from_env("APP_NAME", "FASTAPI")
container.config.logging.level.from_env("LOG_LEVEL", "INFO")
container.config.logging.to_console.from_env("LOG_TO_CONSOLE", True)
container.config.logging.rotation_days.from_env("ROTATION_DAYS", 5)
container.config.logging.file.from_env("LOG_FILE", "logs/app.log")
container.wire(modules=["core.logger.logger_middleware", "api.routes.user_router"])
container.wire(modules=["core.logger.logger_middleware", "api.routes.todo_router"])
container.wire(modules=["core.logger.exception_handlers"])

app.container = container

logger = container.logger()

if not os.path.exists("db.sqlite3"):
    logger.info("📦 Criando banco de dados e tabelas...")
    SQLModel.metadata.create_all(container.engine())
    logger.info("✅ Banco criado com sucesso!")
else:
    logger.info("📁 Banco já existe, sem necessidade de criar.")


# Static Route
app.mount("/static", StaticFiles(directory="static"), name="static")

# REST Routes
app.include_router(user_router.router)
app.include_router(todo_router.router)


# GraphQL Route
def get_context():
    return {
        "todo_service": container.todo_service(),
        "logger": container.logger(),
    }


graphql_app = GraphQLRouter(schema, context_getter=get_context)
app.include_router(graphql_app, prefix="/graphql")

# Middlewares
app.add_middleware(RequestLoggingMiddleware)
app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))

oauth = OAuth()
oauth.register(
    name="google",
    client_id=env.get("GOOGLE_CLIENT_ID", type=str),
    client_secret=env.get("GOOGLE_CLIENT_SECRET", type=str),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse("static/favicon.ico")


@app.get("/")
def read_root():
    return {"message": "Hexagonal Architecture API! "}


@app.get("/login")
async def login(request: Request):
    redirect_uri = env.get("REDIRECT_URI")
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    access_token = create_access_token(
        data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60)
    )

    return RedirectResponse(
        url=f"{env.get('FRONT_REDIRECT_URI', str)}?token={access_token}"
    )


@app.get("/me")
async def me(request: Request):
    token = request.query_params.get("token")
    payload = verify_access_token(token)
    return payload
