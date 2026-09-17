from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import DB, User, Job

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin/login", methods=["POST"])
def admin_login():
    from routes.auth import login as auth_login

    return auth_login()


@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def admin_users():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in User.query.all()])


@admin_bp.route("/admin/jobs", methods=["GET"])
@jwt_required()
def admin_jobs():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify([{"id": j.id, "title": j.title, "location": j.location} for j in Job.query.all()])


@admin_bp.route("/users", methods=["GET"])
@jwt_required()
def users():
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    return jsonify([{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in User.query.all()])


@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    identity = get_jwt_identity()
    if identity["role"] != "admin":
        return jsonify({"error": "Admin access required"}), 403
    user = User.query.get_or_404(user_id)
    DB.session.delete(user)
    DB.session.commit()
    return jsonify({"message": "User deleted successfully"})
