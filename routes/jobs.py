from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import DB, Job, Company, User

jobs_bp = Blueprint("jobs", __name__)


@jobs_bp.route("/jobs", methods=["GET"])
def get_jobs():
    jobs = Job.query.all()
    result = []
    for job in jobs:
        company = Company.query.get(job.company_id)
        result.append({
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "location": job.location,
            "salary": job.salary,
            "skills": job.skills,
            "company": {"id": company.id, "company_name": company.company_name, "location": company.location} if company else None,
        })
    return jsonify(result)


@jobs_bp.route("/jobs/<int:job_id>", methods=["GET"])
def get_job(job_id):
    job = Job.query.get_or_404(job_id)
    company = Company.query.get(job.company_id)
    return jsonify({
        "id": job.id,
        "title": job.title,
        "description": job.description,
        "location": job.location,
        "salary": job.salary,
        "skills": job.skills,
        "company": {"id": company.id, "company_name": company.company_name, "website": company.website, "location": company.location, "description": company.description} if company else None,
    })


@jobs_bp.route("/jobs", methods=["POST"])
@jwt_required()
def create_job():
    identity = get_jwt_identity()
    if identity["role"] not in ("recruiter", "admin"):
        return jsonify({"error": "Only recruiters can create jobs"}), 403

    data = request.get_json(silent=True) or {}
    company = Company.query.filter_by(recruiter_id=identity["id"]).first()
    if not company:
        return jsonify({"error": "Create a company profile first"}), 400

    job = Job(
        title=data.get("title"),
        description=data.get("description"),
        location=data.get("location"),
        salary=data.get("salary"),
        skills=data.get("skills"),
        company_id=company.id,
    )
    DB.session.add(job)
    DB.session.commit()
    return jsonify({"message": "Job posted successfully", "job": {"id": job.id}}), 201


@jobs_bp.route("/jobs/<int:job_id>", methods=["PUT"])
@jwt_required()
def update_job(job_id):
    identity = get_jwt_identity()
    job = Job.query.get_or_404(job_id)
    company = Company.query.filter_by(recruiter_id=identity["id"]).first()
    if identity["role"] != "admin" and (not company or job.company_id != company.id):
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json(silent=True) or {}
    job.title = data.get("title", job.title)
    job.description = data.get("description", job.description)
    job.location = data.get("location", job.location)
    job.salary = data.get("salary", job.salary)
    job.skills = data.get("skills", job.skills)
    DB.session.commit()
    return jsonify({"message": "Job updated successfully"})


@jobs_bp.route("/jobs/<int:job_id>", methods=["DELETE"])
@jwt_required()
def delete_job(job_id):
    identity = get_jwt_identity()
    job = Job.query.get_or_404(job_id)
    company = Company.query.filter_by(recruiter_id=identity["id"]).first()
    if identity["role"] != "admin" and (not company or job.company_id != company.id):
        return jsonify({"error": "Unauthorized"}), 403

    DB.session.delete(job)
    DB.session.commit()
    return jsonify({"message": "Job deleted successfully"})
