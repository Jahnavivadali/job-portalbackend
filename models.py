from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


DB = SQLAlchemy()


class User(DB.Model):
    __tablename__ = "users"

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    email = DB.Column(DB.String(120), unique=True, nullable=False)
    password = DB.Column(DB.String(255), nullable=False)
    role = DB.Column(DB.String(20), nullable=False, default="candidate")
    created_at = DB.Column(DB.DateTime, server_default=DB.text("CURRENT_TIMESTAMP"))

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Company(DB.Model):
    __tablename__ = "companies"

    id = DB.Column(DB.Integer, primary_key=True)
    company_name = DB.Column(DB.String(150), nullable=False)
    website = DB.Column(DB.String(255), nullable=True)
    location = DB.Column(DB.String(150), nullable=True)
    description = DB.Column(DB.Text, nullable=True)
    recruiter_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"), nullable=False)


class Job(DB.Model):
    __tablename__ = "jobs"

    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(150), nullable=False)
    description = DB.Column(DB.Text, nullable=False)
    location = DB.Column(DB.String(150), nullable=True)
    salary = DB.Column(DB.String(100), nullable=True)
    skills = DB.Column(DB.Text, nullable=True)
    company_id = DB.Column(DB.Integer, DB.ForeignKey("companies.id"), nullable=False)
    created_at = DB.Column(DB.DateTime, server_default=DB.text("CURRENT_TIMESTAMP"))


class Application(DB.Model):
    __tablename__ = "applications"

    id = DB.Column(DB.Integer, primary_key=True)
    user_id = DB.Column(DB.Integer, DB.ForeignKey("users.id"), nullable=False)
    job_id = DB.Column(DB.Integer, DB.ForeignKey("jobs.id"), nullable=False)
    resume_path = DB.Column(DB.String(255), nullable=True)
    status = DB.Column(DB.String(30), default="Applied")
    applied_at = DB.Column(DB.DateTime, server_default=DB.text("CURRENT_TIMESTAMP"))
