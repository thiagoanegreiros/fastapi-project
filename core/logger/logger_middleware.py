import datetime
from uuid import uuid4

from dependency_injector.wiring import Provide, inject
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from core.container import Container
from core.logger.logger import Logger
from core.logger.request_context import request_id_ctx_var


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

        logger.info(
            {
                "type": "RequestStatus",
                "method": request.method,
                "path": request.url.path,
                "response_code": response.status_code,
                "duration_ms": int(duration),
                "message": f"{request.method} {request.url.path} completed",
            }
        )

        return response


@inject
def log_with_request(
    request: Request,
    level="INFO",
    data=None,
    logger: Logger = Provide[Container.logger],
):
    request_id = getattr(request.state, "request_id", None)

    match level.upper():
        case "DEBUG":
            logger.debug(data, request_id=request_id)
        case "INFO":
            logger.info(data, request_id=request_id)
        case "WARNING":
            logger.warning(data, request_id=request_id)
        case "ERROR":
            logger.error(data, request_id=request_id)
        case _:
            logger.info(data, request_id=request_id)
