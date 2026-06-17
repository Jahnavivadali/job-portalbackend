import logging
import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from config import Config
from models import DB

logging.basicConfig(
level=logging.INFO,
format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

def create_app():
app = Flask(**name**)

```
app.config.from_object(Config)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": app.config.get(
                "CORS_ORIGINS",
                [
                    "https://job-portal-frontend-zb7g.vercel.app",
                    "http://localhost:3000",
                    "http://localhost:5173",
                ],
            )
        }
    },
    supports_credentials=True,
)

DB.init_app(app)

JWTManager(app)

try:
    if os.getenv("CREATE_DB", "true").lower() in (
        "1",
        "true",
        "yes",
    ):
        with app.app_context():
            DB.create_all()
            app.logger.info(
                "Database tables ensured (DB.create_all())."
            )

except Exception:
    app.logger.exception(
        "Failed to auto-create database tables"
    )

@app.route("/")
def home():
    return jsonify({
        "message": "Job Portal Backend Running"
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "ok"
    })

try:
    from routes.auth import auth_bp
    app.register_blueprint(
        auth_bp,
        url_prefix="/api/auth"
    )
except Exception:
    app.logger.warning(
        "Auth routes not loaded"
    )

try:
    from routes.jobs import jobs_bp
    app.register_blueprint(
        jobs_bp,
        url_prefix="/api/jobs"
    )
except Exception:
    app.logger.warning(
        "Jobs routes not loaded"
    )

return app
```

app = create_app()

if **name** == "**main**":
app.run(
host="0.0.0.0",
port=int(os.getenv("PORT", 5000)),
debug=True,
)
