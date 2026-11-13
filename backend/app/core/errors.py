"""Centralised error handling.

Every error response shares the same envelope, mirrored by the frontend
(`frontend/src/types/api.ts`):

    {"error": {"code": "...", "message": "...", "details": ...}}
"""

import logging
from http import HTTPStatus
from typing import Any

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import OperationalError, SQLAlchemyError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for expected, user-facing application errors."""

    status_code: int = status.HTTP_400_BAD_REQUEST
    code: str = "bad_request"

    def __init__(self, message: str, *, details: Any = None) -> None:
        super().__init__(message)
        self.message = message
        self.details = details


class NotFoundError(AppError):
    status_code = status.HTTP_404_NOT_FOUND
    code = "not_found"


class DatabaseNotConfiguredError(AppError):
    status_code = status.HTTP_503_SERVICE_UNAVAILABLE
    code = "database_not_configured"

    def __init__(self) -> None:
        super().__init__("The database connection is not configured (DATABASE_URL is missing).")


def error_response(status_code: int, code: str, message: str, details: Any = None) -> JSONResponse:
    body: dict[str, Any] = {"error": {"code": code, "message": message}}
    if details is not None:
        body["error"]["details"] = jsonable_encoder(details)
    return JSONResponse(status_code=status_code, content=body)


async def _app_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, AppError)
    return error_response(exc.status_code, exc.code, exc.message, exc.details)


async def _http_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, StarletteHTTPException)
    try:
        default_code = HTTPStatus(exc.status_code).phrase.lower().replace(" ", "_")
    except ValueError:
        default_code = "http_error"
    message = exc.detail if isinstance(exc.detail, str) else HTTPStatus(exc.status_code).phrase
    response = error_response(exc.status_code, default_code, message)
    if exc.headers:
        response.headers.update(exc.headers)
    return response


async def _validation_error_handler(_: Request, exc: Exception) -> JSONResponse:
    assert isinstance(exc, RequestValidationError)
    return error_response(
        status.HTTP_422_UNPROCESSABLE_CONTENT,
        "validation_error",
        "The request is invalid.",
        exc.errors(),
    )


async def _database_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Database error", exc_info=exc)
    if isinstance(exc, OperationalError):
        return error_response(
            status.HTTP_503_SERVICE_UNAVAILABLE,
            "database_unavailable",
            "The database is temporarily unavailable.",
        )
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "database_error", "A database error occurred."
    )


async def _unhandled_error_handler(_: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled error", exc_info=exc)
    return error_response(
        status.HTTP_500_INTERNAL_SERVER_ERROR, "internal_error", "An unexpected error occurred."
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(AppError, _app_error_handler)
    app.add_exception_handler(StarletteHTTPException, _http_error_handler)
    app.add_exception_handler(RequestValidationError, _validation_error_handler)
    app.add_exception_handler(SQLAlchemyError, _database_error_handler)
    app.add_exception_handler(Exception, _unhandled_error_handler)
