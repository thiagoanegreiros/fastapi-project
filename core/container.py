from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.application.movie_service import MovieService
from core.application.todo_service import TodoService
from core.application.user_service import UserService
from core.logger.logger import Logger
from infrastructure.api.movies_api_client import MoviesApiClient
from infrastructure.api.todo_api_client import TodoApiClient
from infrastructure.database.user_repository import UserRepository

DB_PATH = "db.sqlite3"
DATABASE_URL = "sqlite+aiosqlite:///" + DB_PATH  # ✅ async driver


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            "api.routes.user_router",
            "api.routes.todo_router",
            "api.routes.movies_router",
        ]
    )

    config = providers.Configuration()

    # ✅ Engine assíncrono
    engine = providers.Singleton(
        create_async_engine,
        DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=True,
    )

    # ✅ sessionmaker assíncrono
    session_factory = providers.Singleton(
        async_sessionmaker,
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    # ✅ Resource assíncrono (yield para injetar corretamente)
    session = providers.Resource(
        lambda session_factory: session_factory(),
        session_factory,
    )

    logger = providers.Singleton(
        Logger,
        name=config.logging.app,
        level=config.logging.level,
        rotation_days=config.logging.rotation_days,
        log_to_console=config.logging.to_console,
        log_file=config.logging.file,
    )

    user_repository = providers.Factory(UserRepository, session=session)
    user_service = providers.Factory(
        UserService, user_repository=user_repository, logger=logger
    )

    todo_client = TodoApiClient("https://jsonplaceholder.typicode.com")
    todo_service = providers.Factory(TodoService, todo_client, logger=logger)

    movies_client = MoviesApiClient("https://api.themoviedb.org/3")
    movie_service = providers.Factory(MovieService, movies_client, logger=logger)
