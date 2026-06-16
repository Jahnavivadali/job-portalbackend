import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import DB

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s %(message)s')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    DB.init_app(app)

    # Auto-create database tables in development when enabled via env
    try:
        if os.getenv("CREATE_DB", "true").lower() in ("1", "true", "yes"):
            with app.app_context():
                DB.create_all()
                app.logger.info("Database tables ensured (DB.create_all()).")
                # Ensure users.created_at column exists; add it if missing (dev convenience)
                try:
                    from sqlalchemy import inspect, text

                    inspector = inspect(DB.engine)
                    cols = [c["name"] for c in inspector.get_columns("users")] if "users" in inspector.get_table_names() else []
                    if "created_at" not in cols:
                        dialect = DB.engine.dialect.name
                        app.logger.info("Adding missing column 'created_at' to users table (dialect=%s)", dialect)
                        with DB.engine.connect() as conn:
                            if dialect == "mysql":
                                conn.execute(text("ALTER TABLE users ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP"))
                            else:
                                # SQLite and others: add a nullable datetime column
                                conn.execute(text("ALTER TABLE users ADD COLUMN created_at DATETIME"))
                            app.logger.info("Column 'created_at' added to users table")
                except Exception:
                    app.logger.exception("Failed to ensure users.created_at column")
    except Exception:
        app.logger.exception("Failed to auto-create database tables")

    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": app.config["CORS_ORIGINS"],
            }
        },
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )
    JWTManager(app)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    @app.errorhandler(Exception)
    def handle_unhandled_exception(error):
        app.logger.exception("Unhandled exception")
        response = jsonify({"success": False, "message": "Server error occurred."})
        response.status_code = 500
        return response

    from routes.auth import auth_bp
    from routes.jobs import jobs_bp
    from routes.applications import applications_bp
    from routes.recruiter import recruiter_bp
    from routes.admin import admin_bp

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
    port = int(os.getenv("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
