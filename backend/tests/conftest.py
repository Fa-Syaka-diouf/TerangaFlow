from collections.abc import Callable, Iterator

import pytest
from fastapi.testclient import TestClient

from app.core.config import get_settings
from app.db.session import dispose_engine, get_engine, get_session_factory
from app.main import create_app


def _clear_caches() -> None:
    dispose_engine()
    get_settings.cache_clear()
    get_engine.cache_clear()
    get_session_factory.cache_clear()


@pytest.fixture
def make_client(monkeypatch: pytest.MonkeyPatch) -> Iterator[Callable[..., TestClient]]:
    """Build a TestClient for a given environment.

    Environment variables take precedence over `backend/.env`, so tests never
    depend on (nor touch) the developer's local configuration.
    """

    def factory(database_url: str = "", **env: str) -> TestClient:
        monkeypatch.setenv("APP_ENV", "test")
        monkeypatch.setenv("DATABASE_URL", database_url)
        monkeypatch.setenv("DB_CONNECT_TIMEOUT", "2")
        for key, value in env.items():
            monkeypatch.setenv(key.upper(), value)
        _clear_caches()
        return TestClient(create_app(), raise_server_exceptions=False)

    yield factory
    _clear_caches()
