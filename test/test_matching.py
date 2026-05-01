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


def test_get_matches_authenticated(auth_client):
    response = auth_client.get("/api/matches")
    assert response.status_code == 200


def test_get_matches_unauthenticated(app):
    client = app.test_client()
    response = client.get("/api/matches")
    assert response.status_code == 401


def test_get_potential_matches(auth_client):
    response = auth_client.get("/api/matches/potential")
    assert response.status_code in [200, 400]


def test_match_action_invalid_action(auth_client):
    response = auth_client.post("/api/matches/action", json={
        "receiver_id": 1,
        "action": "invalid_action"
    })
    assert response.status_code == 400


def test_match_action_missing_field(auth_client):
    response = auth_client.post("/api/matches/action", json={
        "receiver_id": 1
    })
    assert response.status_code == 400
