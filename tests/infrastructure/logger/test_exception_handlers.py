from unittest.mock import MagicMock

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.testclient import TestClient
from pydantic import BaseModel
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from infrastructure.container import Container
from infrastructure.logger.exception_handlers import (
    global_exception_handler,
    http_exception_handler,
    validation_exception_handler,
)

app = FastAPI()

mock_logger = MagicMock()
container = Container()
container.logger.override(mock_logger)
container.init_resources()
container.wire(modules=["infrastructure.logger.exception_handlers"])
app.container = container

app.add_exception_handler(Exception, global_exception_handler)
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/error")
def raise_error():
    raise Exception("Erro inesperado")


@app.get("/not-found")
def raise_http():
    raise HTTPException(status_code=404, detail="Item não encontrado")


class Input(BaseModel):
    name: str


@app.post("/validate")
def validate_input(data: Input):
    return {"message": f"Olá {data.name}"}


client = TestClient(app, raise_server_exceptions=False)


def test_global_exception_handler():
    response = client.get("/error")
    assert response.status_code == 500
    assert "request_id" in response.json()
    mock_logger.error.assert_called_once()


def test_http_exception_handler():
    response = client.get("/not-found")
    assert response.status_code == 404
    assert "request_id" in response.json()
    mock_logger.warning.assert_called_once()


def test_validation_exception_handler():
    response = client.post("/validate", json={})
    assert response.status_code == HTTP_422_UNPROCESSABLE_ENTITY
    assert "request_id" in response.json()
    mock_logger.warning.assert_called()
