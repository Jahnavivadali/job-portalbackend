import logging
import re

from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import DB, User

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__)

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
VALID_ROLES = {"candidate", "recruiter"}


def make_error(payload, status=400):
    return jsonify(payload), status


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    logger.info("Register body: %s", data)
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    role = (data.get("role") or "").strip().lower()

    errors = {}

    if not name:
        errors["name"] = "Username is required."
    elif len(name) < 2:
        errors["name"] = "Username must be at least 2 characters."

    if not email:
        errors["email"] = "Email is required."
    elif not EMAIL_REGEX.match(email):
        errors["email"] = "Enter a valid email address."
    elif User.query.filter_by(email=email).first():
        errors["email"] = "Email already exists."

    if not password:
        errors["password"] = "Password is required."
    elif len(password) < 8:
        errors["password"] = "Password must be at least 8 characters."

    if not role:
        errors["role"] = "Please choose a role."
    elif role not in VALID_ROLES:
        errors["role"] = "Invalid role selected."

    if errors:
        return make_error({"success": False, "message": "Validation failed.", "errors": errors})

    try:
        user = User(name=name, email=email, role=role)
        user.set_password(password)
        DB.session.add(user)
        DB.session.commit()
        return jsonify({"success": True, "message": "Registration successful"}), 201
    except Exception as exc:
        logger.exception("Failed to register user")
        DB.session.rollback()
        return make_error({"success": False, "message": "Server error during registration."}, 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user:
        return make_error({"success": False, "message": "Email does not exist."}, 401)

    if not user.check_password(password):
        return make_error({"success": False, "message": "Invalid credentials."}, 401)

    token = create_access_token(identity={"id": user.id, "email": user.email, "role": user.role})
    return jsonify({
        "success": True,
        "token": token,
        "user": {"id": user.id, "name": user.name, "email": user.email, "role": user.role},
    })


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    user = User.query.get(identity["id"])
    return jsonify({"id": user.id, "name": user.name, "email": user.email, "role": user.role})


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    return jsonify({"message": "Logged out successfully"})
