from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


def test_health_and_security_headers() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"
        assert response.headers["X-Content-Type-Options"] == "nosniff"
        assert response.headers["X-Frame-Options"] == "DENY"
        assert "Content-Security-Policy" in response.headers


def test_request_id_forwarding() -> None:
    with TestClient(app) as client:
        response = client.get("/health", headers={"X-Request-ID": "my-custom-id"})
        assert response.status_code == 200
        assert response.headers["X-Request-ID"] == "my-custom-id"


def test_rate_limit_protection() -> None:
    with TestClient(app) as client:
        for _ in range(40):
            ok = client.post("/api/v1/echo", json={"message": "hello"})
            assert ok.status_code == 200

        limited = client.post("/api/v1/echo", json={"message": "blocked"})
        assert limited.status_code == 429
