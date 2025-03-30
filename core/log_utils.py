import datetime
import json
import logging
from uuid import uuid4

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def make_log(level, request_id, type_, data):
    log = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "level": level,
        "request_id": request_id,
        "type": type_,
        "data": data,
    }
    logger.info(json.dumps(log))


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid4())
        request.state.request_id = request_id
        start = datetime.datetime.now(datetime.timezone.utc)

        response: Response = await call_next(request)

        duration = (
            datetime.datetime.now(datetime.timezone.utc) - start
        ).total_seconds() * 1000

        make_log(
            "INFO",
            request_id,
            "RequestStatus",
            {
                "method": request.method,
                "path": request.url.path,
                "response_code": response.status_code,
                "duration_ms": int(duration),
                "message": f"{request.method} {request.url.path} completed",
            },
        )

        return response


def log_with_request(request: Request, level="INFO", data=None):
    request_id = getattr(request.state, "request_id", str(uuid4()))
    make_log(level, request_id, "Log", data or {})
