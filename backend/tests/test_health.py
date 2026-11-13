import os

import pytest


def test_health_returns_service_metadata(make_client):
    response = make_client().get("/api/v1/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "TerangaFlow API"
    assert body["environment"] == "test"
    assert "timestamp" in body


def test_database_health_without_configuration_returns_503(make_client):
    response = make_client(database_url="").get("/api/v1/health/database")

    assert response.status_code == 503
    body = response.json()
    assert body["status"] == "unavailable"
    assert "DATABASE_URL" in body["detail"]


def test_database_health_with_unreachable_database_hides_details(make_client):
    # Port 1 on localhost: connection refused immediately.
    client = make_client(database_url="postgresql://user:s3cret@127.0.0.1:1/db")
    response = client.get("/api/v1/health/database")

    assert response.status_code == 503
    assert response.json()["detail"] == "Unable to connect to the database."
    assert "s3cret" not in response.text


@pytest.mark.skipif(
    not os.getenv("TEST_DATABASE_URL"),
    reason="Set TEST_DATABASE_URL to run the live database check.",
)
def test_database_health_with_live_database(make_client):
    client = make_client(database_url=os.environ["TEST_DATABASE_URL"])
    response = client.get("/api/v1/health/database")

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["status"] == "ok"
    assert body["database"].startswith("PostgreSQL")
    assert body["latency_ms"] >= 0


def test_swagger_and_openapi_are_served(make_client):
    client = make_client()
    assert client.get("/docs").status_code == 200
    schema = client.get("/api/v1/openapi.json").json()
    assert {"/api/v1/health", "/api/v1/health/database"} <= set(schema["paths"])
