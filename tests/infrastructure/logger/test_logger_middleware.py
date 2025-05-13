from unittest.mock import MagicMock

import pytest
from fastapi import Request

from infrastructure.logger.logger_middleware import log_with_request


class DummyReceive:
    async def __call__(self):
        return {"type": "http.request"}


@pytest.mark.parametrize(
    "level,method",
    [
        ("DEBUG", "debug"),
        ("INFO", "info"),
        ("WARNING", "warning"),
        ("ERROR", "error"),
        ("CUSTOM", "info"),  # fallback
    ],
)
def test_log_with_request_calls_correct_logger_method(level, method):
    scope = {
        "type": "http",
        "method": "GET",
        "path": "/test",
        "headers": [],
        "client": ("127.0.0.1", 1234),
        "server": ("testserver", 80),
        "scheme": "http",
        "query_string": b"",
        "root_path": "",
    }

    request = Request(scope, DummyReceive())
    request.state.request_id = "mocked-request-id"

    mock_logger = MagicMock()

    log_with_request(
        request=request, level=level, data={"foo": "bar"}, logger=mock_logger
    )

    getattr(mock_logger, method).assert_called_once_with(
        {"foo": "bar"}, request_id="mocked-request-id"
    )
