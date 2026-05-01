import pytest
from app import create_app, db


@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_ENGINE_OPTIONS": {}
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


def test_config_loaded(app):
    assert app.config["SECRET_KEY"] is not None
    assert "SQLALCHEMY_DATABASE_URI" in app.config


def test_testing_flag(app):
    assert app.config["TESTING"] is True
