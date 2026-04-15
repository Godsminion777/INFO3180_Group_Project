def test_config_loaded(app):
    assert app.config["SECRET_KEY"] is not None
    assert "SQLALCHEMY_DATABASE_URI" in app.config
    