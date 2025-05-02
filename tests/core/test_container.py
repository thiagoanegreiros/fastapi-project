import pytest_asyncio
from dependency_injector import providers
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel import SQLModel

from core.container import Container


@pytest_asyncio.fixture
async def test_container(tmp_path):
    """Cria um container com um banco SQLite assíncrono temporário para testes"""
    db_path = tmp_path / "test_db.sqlite3"
    test_db_url = f"sqlite+aiosqlite:///{db_path}"

    # Cria a engine assíncrona e inicializa o schema do banco
    engine = create_async_engine(test_db_url, connect_args={"check_same_thread": False})
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Configura o container para usar o banco temporário
    container = Container()
    container.config.logging.level.from_value("DEBUG")
    container.config.logging.to_console.from_value(False)
    container.config.logging.rotation_days.from_value(1)
    container.config.logging.file.from_value(None)

    # ✅ Corrigido: passa a instância real do engine para o provider
    container.engine.override(providers.Object(engine))

    yield container

    container.unwire()
    del container
