from app.core.config import Settings


def test_unknown_route_uses_error_envelope(make_client):
    response = make_client().get("/api/v1/does-not-exist")

    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Not Found"}}


def test_cors_allows_configured_frontend_origin(make_client):
    client = make_client(cors_origins="http://localhost:5173")
    response = client.options(
        "/api/v1/health",
        headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "GET"},
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://localhost:5173"


def test_cors_rejects_unknown_origin(make_client):
    client = make_client(cors_origins="http://localhost:5173")
    response = client.options(
        "/api/v1/health",
        headers={"Origin": "https://evil.example", "Access-Control-Request-Method": "GET"},
    )

    assert "access-control-allow-origin" not in response.headers


def test_settings_normalise_supabase_url_and_origins():
    settings = Settings(
        _env_file=None,  # type: ignore[call-arg]
        database_url="postgres://postgres.ref:pw@aws-0-eu-west-3.pooler.supabase.com:5432/postgres",
        cors_origins="http://localhost:5173/, http://127.0.0.1:5173",
    )

    assert settings.sqlalchemy_database_url.startswith("postgresql+psycopg://postgres.ref:pw@")
    assert settings.cors_origins == ["http://localhost:5173", "http://127.0.0.1:5173"]
    assert "pw" not in repr(settings)
