from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, Request

from core.auth import create_access_token, require_auth


def generate_test_token():
    return create_access_token(data={"sub": "test@example.com"})


def test_require_auth_succeeds():
    token = generate_test_token()
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": f"Bearer {token}"}

    payload = require_auth(mock_request)
    assert payload["sub"] == "test@example.com"


def test_require_auth_missing_authorization_header():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {}

    with pytest.raises(HTTPException) as exc_info:
        require_auth(mock_request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"


def test_require_auth_invalid_authorization_format():
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "InvalidTokenFormat"}

    with pytest.raises(HTTPException) as exc_info:
        require_auth(mock_request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"


def test_require_auth_invalid_token():
    # Aqui é um token inválido mesmo (não JWT válido)
    mock_request = MagicMock(spec=Request)
    mock_request.headers = {"Authorization": "Bearer invalid.token.here"}

    with pytest.raises(HTTPException) as exc_info:
        require_auth(mock_request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Invalid token"
