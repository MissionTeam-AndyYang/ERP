from app.main import app


client = app.test_client()


def test_health_check() -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"
