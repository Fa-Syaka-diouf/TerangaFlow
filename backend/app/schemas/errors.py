from typing import Any

from pydantic import BaseModel


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Any | None = None


class ErrorResponse(BaseModel):
    """Envelope returned by every error (see `app/core/errors.py`)."""

    error: ErrorDetail
