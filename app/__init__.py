from flask import Flask, app, send_from_directory
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models

    CORS(
    app,
    resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    supports_credentials=True
    )
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.views.profile import profiles_bp
    app.register_blueprint(profiles_bp, url_prefix='/api/profiles')

    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(os.getenv('UPLOAD_FOLDER'), filename)

    return app