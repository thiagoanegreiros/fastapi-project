from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException, Request

from core.auth import require_auth


def test_require_auth_succeeds():
    mock_request = MagicMock(spec=Request)
    mock_request.session = {"user": {"email": "test@example.com"}}

    user = require_auth(mock_request)
    assert user["email"] == "test@example.com"


def test_require_auth_unauthenticated():
    mock_request = MagicMock(spec=Request)
    mock_request.session = {}  # No "user" key

    with pytest.raises(HTTPException) as exc_info:
        require_auth(mock_request)

    assert exc_info.value.status_code == 401
    assert exc_info.value.detail == "Not authenticated"
