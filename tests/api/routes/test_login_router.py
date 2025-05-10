from datetime import timedelta
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

from api.routes import login_router
from core.auth import create_access_token


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(login_router.router)
    return TestClient(app)


def test_refresh_token_valid(client):
    refresh_token = create_access_token(
        data={"sub": "user@example.com"}, expires_delta=timedelta(minutes=5)
    )

    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})

    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_token_invalid(client):
    response = client.post(
        "/auth/refresh", json={"refresh_token": "invalid.token.value"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


def test_me_with_valid_token(client):
    token = create_access_token(
        data={"sub": "user@example.com"}, expires_delta=timedelta(minutes=5)
    )

    response = client.get(f"/me?token={token}")
    assert response.status_code == 200
    assert response.json()["sub"] == "user@example.com"


def test_me_with_invalid_token(client):
    response = client.get("/me?token=invalid.token")
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"


@pytest.mark.asyncio
@patch(
    "api.routes.login_router.oauth.google.authorize_access_token",
    new_callable=AsyncMock,
)
async def test_auth_redirect(mock_auth):
    mock_auth.return_value = {"userinfo": {"email": "user@example.com"}}

    app = FastAPI()
    app.include_router(login_router.router)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        state = "redirect_uri=http://localhost:3000/callback"
        response = await ac.get(f"/auth?state={state}", follow_redirects=False)

    assert response.status_code in (302, 307)
    location = response.headers["location"]
    assert location.startswith("http://localhost:3000/callback")
    assert "token=" in location
    assert "refresh_token=" in location


@pytest.mark.asyncio
@patch(
    "api.routes.login_router.oauth.google.authorize_redirect", new_callable=AsyncMock
)
async def test_login_redirect(mock_redirect):
    mock_redirect.return_value = "mocked redirect response"

    app = FastAPI()
    app.include_router(login_router.router)

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.get("/login?redirect_uri=http://localhost:3000/callback")

    assert response.status_code == 200
    assert response.text == '"mocked redirect response"'

    mock_redirect.assert_awaited_once()
