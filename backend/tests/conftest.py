import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Register + login a test user, return auth headers."""
    import json
    client.post(
        "/api/auth/register",
        data=json.dumps({"name": "Test User", "email": "test@example.com", "password": "password123"}),
        content_type="application/json",
    )
    res = client.post(
        "/api/auth/login",
        data=json.dumps({"email": "test@example.com", "password": "password123"}),
        content_type="application/json",
    )
    token = res.get_json()["data"]["token"]
    return {"Authorization": f"Bearer {token}"}
