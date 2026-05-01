import pytest
from app import create_app, db

VALID_USER = {
    "email": "test@example.com",
    "username": "testuser",
    "password": "password123",
    "first_name": "Test",
    "last_name": "User",
    "age": 25,
    "gender": "male",
    "looking_for": "any"
}


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {},
        "SECRET_KEY": "test-secret"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def auth_client(app):
    client = app.test_client()
    client.post("/api/auth/register", json=VALID_USER)
    client.post("/api/auth/login", json={
        "email": VALID_USER["email"],
        "password": VALID_USER["password"]
    })
    return client


def test_send_message_requires_auth(app):
    client = app.test_client()
    response = client.post("/api/messages", json={
        "receiver_id": 1,
        "content": "Hello!"
    })
    assert response.status_code == 401


def test_send_message_not_matched(auth_client):
    response = auth_client.post("/api/messages", json={
        "receiver_id": 999,
        "content": "Hello!"
    })
    assert response.status_code == 403


def test_send_message_missing_field(auth_client):
    response = auth_client.post("/api/messages", json={
        "receiver_id": 1
    })
    assert response.status_code == 400


def test_get_conversations_authenticated(auth_client):
    response = auth_client.get("/api/messages/conversations")
    assert response.status_code == 200


def test_get_conversations_unauthenticated(app):
    client = app.test_client()
    response = client.get("/api/messages/conversations")
    assert response.status_code == 401
