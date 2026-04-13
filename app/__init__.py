from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    CORS(
    app,
    resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    supports_credentials=True
     )

    return app