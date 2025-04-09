import datetime
import json
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.container import Container
from core.logger.logger import Logger
from core.logger.request_context import request_id_ctx_var


def make_log(level, request_id, type_, data, logger):
    log = {
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "level": level,
        "request_id": request_id,
        "type": type_,
        "data": data,
    }

    log_str = json.dumps(log)

    match level.upper():
        case "INFO":
            logger.info(log_str)
        case "ERROR":
            logger.error(log_str)
        case "WARNING":
            logger.warning(log_str)
        case "DEBUG":
            logger.debug(log_str)
        case _:
            logger.info(log_str)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    @inject
    async def dispatch(
        self, request: Request, call_next, logger: Logger = Provide[Container.logger]
    ):
        request_id = str(uuid4())

        request_id_ctx_var.set(request_id)

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
            logger.get_logger(),
        )

        return response


@inject
def log_with_request(
    request: Request,
    level="INFO",
    data=None,
    logger: Logger = Provide[Container.logger],
):
    request_id = getattr(request.state, "request_id", str(uuid4()))
    make_log(level, request_id, "Log", data or {}, logger.get_logger())
