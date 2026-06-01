import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///village_jobs.db'
    
    # Fix for Heroku PostgreSQL URL (postgres:// -> postgresql://)
    if DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Upload settings
    UPLOAD_FOLDER = 'static/uploads'
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    
    # Pagination
    JOBS_PER_PAGE = 10
    WORKERS_PER_PAGE = 20
    
    # Job categories
    JOB_CATEGORIES = [
        'Agriculture',
        'Construction',
        'Services',
        'Local Business',
        'Government Works'
    ]
    
    # Skills list
    SKILLS_LIST = [
        'Harvesting', 'Planting', 'Irrigation', 'Dairy Farm Work',
        'Mason', 'Painter', 'Labor Helper', 'Carpenter',
        'Electrician', 'Plumber', 'Driver', 'Housekeeping',
        'Shop Assistant', 'Delivery Partner', 'Warehouse Helper',
        'Road Construction', 'Water Conservation', 'Plantation'
    ]
