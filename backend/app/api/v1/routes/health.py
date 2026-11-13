import logging
import time
from datetime import UTC, datetime
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import Settings, get_settings
from app.core.errors import DatabaseNotConfiguredError
from app.db.session import get_engine
from app.schemas.health import DatabaseHealthResponse, HealthResponse

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("", response_model=HealthResponse, summary="API liveness check")
def health(settings: Annotated[Settings, Depends(get_settings)]) -> HealthResponse:
    return HealthResponse(
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        timestamp=datetime.now(UTC),
    )


def _unavailable(detail: str) -> JSONResponse:
    payload = DatabaseHealthResponse(status="unavailable", database="postgresql", detail=detail)
    return JSONResponse(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, content=payload.model_dump())


@router.get(
    "/database",
    response_model=DatabaseHealthResponse,
    summary="Database connectivity check",
    responses={
        status.HTTP_503_SERVICE_UNAVAILABLE: {
            "description": "Database not configured or unreachable",
            "model": DatabaseHealthResponse,
        }
    },
)
def database_health() -> DatabaseHealthResponse | JSONResponse:
    """Runs `SELECT version()` against PostgreSQL and reports the round-trip latency."""
    try:
        engine = get_engine()
    except DatabaseNotConfiguredError as exc:
        return _unavailable(exc.message)

    started = time.perf_counter()
    try:
        with engine.connect() as connection:
            version = connection.execute(text("SELECT version()")).scalar_one()
    except SQLAlchemyError as exc:
        # Log server-side only; never leak connection details to clients.
        logger.warning("Database health check failed: %s", exc.__class__.__name__, exc_info=exc)
        return _unavailable("Unable to connect to the database.")

    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    return DatabaseHealthResponse(
        status="ok",
        database=" ".join(str(version).split()[:2]),  # e.g. "PostgreSQL 17.4"
        latency_ms=latency_ms,
    )
