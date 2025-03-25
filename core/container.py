from dependency_injector import containers, providers

from core.application.user_service import UserService
from infrastructure.database.user_repository import UserRepository


class Container(containers.DeclarativeContainer):
    """Container de injeção de dependência"""

    wiring_config = containers.WiringConfiguration(
        modules=["api.routes.user_router"]
    )

    user_repository = providers.Singleton(UserRepository)
    user_service = providers.Singleton(UserService, user_repository)
