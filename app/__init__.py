from flask import Flask, send_from_directory
import os
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
from werkzeug.utils import secure_filename

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    from app import models
    os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
    CORS(
    app,
    resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}},
    supports_credentials=True
    )
    from app.views.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    from app.views.profile import profiles_bp
    app.register_blueprint(profiles_bp, url_prefix='/api/profiles')
    
    @app.route("/")
    def health():
        return {
            "message": "DriftDater API running"
        }
    
    @app.route('/uploads/<path:filename>')
    def uploaded_file(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)
    
    from app.views.matches import matches_bp
    app.register_blueprint(matches_bp, url_prefix='/api/matches')

    from app.views.messages import messages_bp
    app.register_blueprint(messages_bp, url_prefix='/api/messages')

    return app