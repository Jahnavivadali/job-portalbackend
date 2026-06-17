import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import DB
from routes.auth import auth_bp
from routes.jobs import jobs_bp
from routes.applications import applications_bp
from routes.recruiter import recruiter_bp
from routes.admin import admin_bp


logging.basicConfig(level=logging.INFO)


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    DB.init_app(app)
    JWTManager(app)

    CORS(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    with app.app_context():
        try:
            DB.create_all()
            app.logger.info("Database tables ensured")
        except Exception:
            app.logger.exception("Database error")

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(jobs_bp, url_prefix="/api/jobs")
    app.register_blueprint(applications_bp, url_prefix="/api/applications")
    app.register_blueprint(recruiter_bp, url_prefix="/api/recruiter")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/")
    def health():
        return "Backend running"

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True,
    )
