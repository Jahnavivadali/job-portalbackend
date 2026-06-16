import os

from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename

from config import Config
from models import DB, Application, Job

applications_bp = Blueprint("applications", __name__)


@applications_bp.route("/apply", methods=["POST"])
@jwt_required()
def apply_job():
    identity = get_jwt_identity()
    if identity["role"] != "candidate":
        return jsonify({"error": "Only candidates can apply"}), 403

    if "resume" not in request.files:
        return jsonify({"error": "Resume file is required"}), 400

    file = request.files["resume"]
    job_id = request.form.get("job_id")

    if not file.filename:
        return jsonify({"error": "Resume file is required"}), 400

    filename = secure_filename(file.filename)
    upload_dir = Config.UPLOAD_FOLDER
    os.makedirs(upload_dir, exist_ok=True)
    file_path = os.path.join(upload_dir, f"{identity['id']}_{job_id}_{filename}")
    file.save(file_path)

    app = Application(user_id=identity["id"], job_id=int(job_id), resume_path=file_path, status="Applied")
    DB.session.add(app)
    DB.session.commit()

    return jsonify({"message": "Application submitted successfully", "application": {"id": app.id, "status": app.status}}), 201


@applications_bp.route("/applications", methods=["GET"])
@jwt_required()
def get_applications():
    identity = get_jwt_identity()
    if identity["role"] == "candidate":
        apps = Application.query.filter_by(user_id=identity["id"]).all()
    else:
        apps = Application.query.all()

    result = []
    for app in apps:
        job = Job.query.get(app.job_id)
        result.append({
            "id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else None,
            "status": app.status,
            "resume_path": app.resume_path,
            "applied_at": app.applied_at.isoformat() if app.applied_at else None,
        })
    return jsonify(result)
