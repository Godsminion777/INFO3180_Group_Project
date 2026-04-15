import pytest
from app import create_app, db

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()


def test_register_user(client):
    response = client.post("/api/users", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201


def test_login_valid(client):
    client.post("/api/users", json={
        "email": "test@example.com",
        "password": "password123"
    })

    response = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "password123"
    })

    assert response.status_code == 200


def test_login_invalid(client):
    response = client.post("/api/login", json={
        "email": "wrong@example.com",
        "password": "wrongpass"
    })

    assert response.status_code == 401