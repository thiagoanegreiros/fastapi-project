# tests/test_container.py

import pytest

from core.application.user_service import UserService
from core.container import Container


@pytest.fixture
def test_container(tmp_path):
    """Cria um container com um banco SQLite em memória para testes"""
    db_path = tmp_path / "test_db.sqlite3"
    test_db_url = f"sqlite:///{db_path}"

    container = Container()

    container.config.logging.level.from_value("DEBUG")
    container.config.logging.to_console.from_value(False)
    container.config.logging.rotation_days.from_value(1)
    container.config.logging.file.from_value(None)

    container.override_providers(
        engine=container.engine.override(
            lambda: Container.engine.provider_cls(
                test_db_url, connect_args={"check_same_thread": False}
            )
        )
    )

    # Força a criação do banco no local temporário
    from sqlmodel import SQLModel, create_engine

    engine = create_engine(test_db_url, connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)

    yield container

    # Cleanup
    container.unwire()
    del container


def test_user_service_instantiation(test_container):
    """Verifica se o user_service é instanciado corretamente"""
    service = test_container.user_service()
    assert isinstance(service, UserService)
