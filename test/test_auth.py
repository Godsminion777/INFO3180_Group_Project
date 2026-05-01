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
        "WTF_CSRF_ENABLED": False,
        "SECRET_KEY": "test-secret"
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def test_register_user(client):
    response = client.post("/api/auth/register", json=VALID_USER)
    assert response.status_code == 201


def test_register_duplicate_email(client):
    client.post("/api/auth/register", json=VALID_USER)
    response = client.post("/api/auth/register", json=VALID_USER)
    assert response.status_code == 409


def test_register_missing_field(client):
    response = client.post("/api/auth/register", json={"email": "x@x.com"})
    assert response.status_code == 400


def test_login_valid(client):
    client.post("/api/auth/register", json=VALID_USER)
    response = client.post("/api/auth/login", json={
        "email": VALID_USER["email"],
        "password": VALID_USER["password"]
    })
    assert response.status_code == 200


def test_login_invalid_password(client):
    client.post("/api/auth/register", json=VALID_USER)
    response = client.post("/api/auth/login", json={
        "email": VALID_USER["email"],
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_login_invalid_email(client):
    response = client.post("/api/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })
    assert response.status_code == 401


def test_logout(client):
    client.post("/api/auth/register", json=VALID_USER)
    client.post("/api/auth/login", json={
        "email": VALID_USER["email"],
        "password": VALID_USER["password"]
    })
    response = client.post("/api/auth/logout")
    assert response.status_code == 200


def test_get_current_user_authenticated(client):
    client.post("/api/auth/register", json=VALID_USER)
    client.post("/api/auth/login", json={
        "email": VALID_USER["email"],
        "password": VALID_USER["password"]
    })
    response = client.get("/api/auth/me")
    assert response.status_code == 200


def test_get_current_user_unauthenticated(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
