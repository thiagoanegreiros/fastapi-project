from dependency_injector import containers, providers
from sqlmodel import Session, create_engine

from core.application.todo_service import TodoService
from core.application.user_service import UserService
from core.logger.logger import Logger
from infrastructure.api.todo_api_client import TodoApiClient
from infrastructure.database.user_repository import UserRepository

DB_PATH = "db.sqlite3"
DATABASE_URL = "sqlite:///" + DB_PATH


class Container(containers.DeclarativeContainer):
    """Container de injeção de dependência"""

    wiring_config = containers.WiringConfiguration(modules=["api.routes.user_router"])
    wiring_config = containers.WiringConfiguration(modules=["api.routes.todo_router"])

    # Cria o engine como singleton (não copia)
    engine = providers.Singleton(
        create_engine, DATABASE_URL, connect_args={"check_same_thread": False}
    )

    session = providers.Resource(lambda engine: Session(engine), engine)

    config = providers.Configuration()

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
