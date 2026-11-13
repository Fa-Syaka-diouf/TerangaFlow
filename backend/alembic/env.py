"""Alembic environment.

The database URL comes from `DATABASE_URL` (environment or `backend/.env`)
through the application settings — it is never written in alembic.ini.
"""

from logging.config import fileConfig

from alembic import context
from app.core.config import get_settings
from app.db.session import build_engine
from app.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata
settings = get_settings()

# Used only to render SQL in offline mode when no database is configured.
OFFLINE_PLACEHOLDER_URL = "postgresql+psycopg://"

COMPARE_OPTIONS = {"compare_type": True, "compare_server_default": True}


def run_migrations_offline() -> None:
    """Emit the SQL script without connecting (`alembic upgrade head --sql`)."""
    url = (
        settings.sqlalchemy_database_url
        if settings.is_database_configured
        else OFFLINE_PLACEHOLDER_URL
    )
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **COMPARE_OPTIONS,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    if not settings.is_database_configured:
        raise RuntimeError(
            "DATABASE_URL is not set. Copy backend/.env.example to backend/.env and fill it in."
        )
    connectable = build_engine(settings, null_pool=True)

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, **COMPARE_OPTIONS)
        with context.begin_transaction():
            context.run_migrations()
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
