from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """Base user model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # admin, employer, worker
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Worker(db.Model):
    """Worker/Villager profile"""
    __tablename__ = 'workers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    skills = db.Column(db.String(500))  # Comma-separated skills
    education = db.Column(db.String(100))
    experience = db.Column(db.Integer, default=0)  # Years of experience
    profile_photo = db.Column(db.String(255))
    rating = db.Column(db.Float, default=0.0)
    total_jobs_completed = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='worker_profile')
    applications = db.relationship('Application', backref='worker', lazy='dynamic')
    employment_history = db.relationship('EmploymentHistory', backref='worker', lazy='dynamic')


class Employer(db.Model):
    """Employer profile"""
    __tablename__ = 'employers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    business_type = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(15), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255))
    approval_status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='employer_profile')
    jobs = db.relationship('Job', backref='employer', lazy='dynamic')


class Job(db.Model):
    """Job posting"""
    __tablename__ = 'jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    required_skills = db.Column(db.String(500))
    wage = db.Column(db.Float, nullable=False)
    wage_type = db.Column(db.String(20), default='daily')  # daily, weekly, monthly, per_task
    location = db.Column(db.String(100), nullable=False)
    village = db.Column(db.String(100), nullable=False)
    vacancies = db.Column(db.Integer, default=1)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(20), default='open')  # open, closed, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    applications = db.relationship('Application', backref='job', lazy='dynamic')


class Application(db.Model):
    """Job application"""
    __tablename__ = 'applications'
    
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    message = db.Column(db.Text)
    
    # Unique constraint to prevent duplicate applications
    __table_args__ = (db.UniqueConstraint('worker_id', 'job_id', name='unique_application'),)


class EmploymentHistory(db.Model):
    """Employment history and earnings"""
    __tablename__ = 'employment_history'
    
    id = db.Column(db.Integer, primary_key=True)
    worker_id = db.Column(db.Integer, db.ForeignKey('workers.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employers.id'), nullable=False)
    earning = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date)
    completion_date = db.Column(db.Date)
    worker_rating = db.Column(db.Integer)  # 1-5 rating by employer
    employer_rating = db.Column(db.Integer)  # 1-5 rating by worker
    feedback = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    job = db.relationship('Job', backref='employment_records')
    employer = db.relationship('Employer', backref='employment_records')


class Admin(db.Model):
    """Admin profile"""
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    designation = db.Column(db.String(100))
    contact = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='admin_profile')
