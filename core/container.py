from dependency_injector import containers, providers
from sqlmodel import create_engine, Session, SQLModel
import os

from infrastructure.database.user_repository import UserRepository
from core.application.user_service import UserService

DB_PATH = 'db.sqlite3'
DATABASE_URL = "sqlite:///" + DB_PATH

class Container(containers.DeclarativeContainer):
    """Container de injeção de dependência"""

    wiring_config = containers.WiringConfiguration(
        modules=["api.routes.user_router"]
    )

    # Cria o engine como singleton (não copia)
    engine = providers.Singleton(
        create_engine,
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

    session = providers.Resource(
        lambda engine: Session(engine),
        engine
    )

    user_repository = providers.Factory(UserRepository, session=session)
    user_service = providers.Factory(UserService, user_repository=user_repository)
