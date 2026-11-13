"""SQLAlchemy engine and session management.

The engine is created lazily so that the API can start (and serve
`/health`) even before DATABASE_URL is provided.

Supabase notes
--------------
* Direct connection / session pooler (port 5432): a regular client-side
  connection pool is used.
* Transaction pooler (Supavisor, port 6543): connections are already pooled
  server-side and prepared statements are not supported, so we disable the
  client pool (NullPool) and psycopg's automatic prepared statements.
"""

from collections.abc import Iterator
from functools import lru_cache
from typing import Any

from sqlalchemy import Engine, create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from app.core.config import Settings, get_settings
from app.core.errors import DatabaseNotConfiguredError

SUPABASE_TRANSACTION_POOLER_PORT = 6543


def build_engine(settings: Settings, *, null_pool: bool = False) -> Engine:
    """Create an engine. `null_pool=True` for short-lived processes (migrations, scripts)."""
    url = make_url(settings.sqlalchemy_database_url)
    connect_args: dict[str, Any] = {
        "connect_timeout": settings.db_connect_timeout,
        "application_name": "terangaflow-api",
    }
    engine_kwargs: dict[str, Any] = {"echo": settings.db_echo, "pool_pre_ping": True}

    if url.port == SUPABASE_TRANSACTION_POOLER_PORT:
        connect_args["prepare_threshold"] = None
    if null_pool or url.port == SUPABASE_TRANSACTION_POOLER_PORT:
        engine_kwargs["poolclass"] = NullPool
    else:
        engine_kwargs.update(
            pool_size=settings.db_pool_size,
            max_overflow=settings.db_max_overflow,
            pool_timeout=settings.db_pool_timeout,
            pool_recycle=settings.db_pool_recycle,
        )

    return create_engine(url, connect_args=connect_args, **engine_kwargs)


@lru_cache
def get_engine() -> Engine:
    settings = get_settings()
    if not settings.is_database_configured:
        raise DatabaseNotConfiguredError()
    return build_engine(settings)


@lru_cache
def get_session_factory() -> sessionmaker[Session]:
    return sessionmaker(bind=get_engine(), autoflush=False, expire_on_commit=False)


def get_db() -> Iterator[Session]:
    """FastAPI dependency: one session per request, always closed.

    Write endpoints are responsible for calling `session.commit()`;
    anything left uncommitted is rolled back when the session closes.
    """
    session = get_session_factory()()
    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def dispose_engine() -> None:
    """Close pooled connections (called on application shutdown)."""
    if get_engine.cache_info().currsize:
        get_engine().dispose()
