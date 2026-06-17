import os
import logging

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import DB


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

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=True,
    )
