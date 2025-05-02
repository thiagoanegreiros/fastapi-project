import os
from contextlib import asynccontextmanager
from datetime import timedelta
from urllib.parse import parse_qs, urlencode

from authlib.integrations.starlette_client import OAuth
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.openapi.utils import get_openapi
from fastapi.requests import Request
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import SQLModel
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware
from strawberry.fastapi import GraphQLRouter
from ta_envy import Env

from api.graphql.schema import schema
from api.routes import movies_router, todo_router, user_router
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

@asynccontextmanager
async def lifespan(_: FastAPI):
    if not os.path.exists("db.sqlite3"):
        logger.info("📦 Creating database and tables...")
        async with container.engine().begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("✅ Database created successfully!")
    else:
        logger.info("📁 Database already exists. No need to create.")
    yield

app = FastAPI(lifespan=lifespan)

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
container.wire(modules=["core.logger.logger_middleware", "api.routes.movies_router"])
container.wire(modules=["core.logger.exception_handlers"])

app.container = container

logger = container.logger()

# Static Route
app.mount("/static", StaticFiles(directory="static"), name="static")

# REST Routes
app.include_router(user_router.router)
app.include_router(todo_router.router)
app.include_router(movies_router.router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API com autenticação via Bearer Token JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for operation in path.values():
            operation["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


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
    frontend_redirect_uri = request.query_params.get("redirect_uri")

    state = urlencode({"redirect_uri": frontend_redirect_uri})
    return await oauth.google.authorize_redirect(request, redirect_uri, state=state)


@app.get("/auth")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user_info = token["userinfo"]

    state_raw = request.query_params.get("state", "")
    state_data = parse_qs(state_raw)
    redirect_uri = state_data.get("redirect_uri", [env.get("FRONT_REDIRECT_URI")])[0]

    access_token = create_access_token(
        data={"sub": user_info["email"]}, expires_delta=timedelta(minutes=60)
    )

    return RedirectResponse(url=f"{redirect_uri}?token={access_token}")


@app.get("/me")
async def me(request: Request):
    token = request.query_params.get("token")
    payload = verify_access_token(token)
    return payload
