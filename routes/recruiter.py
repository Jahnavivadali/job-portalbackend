from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import DB, Company

recruiter_bp = Blueprint("recruiter", __name__)


@recruiter_bp.route("/company", methods=["POST"])
@jwt_required()
def create_company():
    identity = get_jwt_identity()
    if identity["role"] not in ("recruiter", "admin"):
        return jsonify({"error": "Only recruiters can create companies"}), 403

    data = request.get_json(silent=True) or {}
    existing = Company.query.filter_by(recruiter_id=identity["id"]).first()
    if existing:
        return jsonify({"error": "Company already exists"}), 400

    company = Company(
        company_name=data.get("company_name"),
        website=data.get("website"),
        location=data.get("location"),
        description=data.get("description"),
        recruiter_id=identity["id"],
    )
    DB.session.add(company)
    DB.session.commit()
    return jsonify({"message": "Company profile created", "company": {"id": company.id}}), 201


@recruiter_bp.route("/recruiter/applicants", methods=["GET"])
@jwt_required()
def applicants():
    identity = get_jwt_identity()
    if identity["role"] != "recruiter":
        return jsonify({"error": "Unauthorized"}), 403
    return jsonify([])
