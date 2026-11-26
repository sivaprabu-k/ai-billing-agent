
def test_database_connection(db_session):
    result = db_session.execute(
        __import__("sqlalchemy").text("SELECT 1")
    ).scalar_one()

    assert result == 1


def test_root_endpoint(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == (
        "AI Billing & Dispute Resolution System is running"
    )


def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
