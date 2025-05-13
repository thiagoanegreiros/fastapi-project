from dependency_injector.wiring import Provide, inject
from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from infrastructure.container import Container


@inject
async def global_exception_handler(
    request: Request,
    exc: Exception,
    logger=Provide[Container.logger],
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.error(
        f"[500] Unhandled exception | request_id={request_id} | path={request.url.path}",
        exc_info=exc,
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "request_id": request_id},
    )


@inject
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
    logger=Provide[Container.logger],
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        f"[{exc.status_code}] HTTPException | request_id={request_id} | path={request.url.path} | detail={exc.detail}",
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "request_id": request_id},
    )


@inject
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
    logger=Provide[Container.logger],
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.warning(
        f"[422] Validation error | request_id={request_id} | path={request.url.path} | errors={exc.errors()}",
        extra={"request_id": request_id},
    )
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "request_id": request_id},
    )
