from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user
from config import Config
from models import db, User
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Ensure required directories exist with proper permissions
    for directory in ['static/uploads', 'reports']:
        os.makedirs(directory, exist_ok=True)
        os.chmod(directory, 0o755)
    
    # Flask automatically creates instance folder with proper permissions
    
    # Initialize extensions
    db.init_app(app)
    
    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.employer import employer_bp
    from routes.worker import worker_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(employer_bp, url_prefix='/employer')
    app.register_blueprint(worker_bp, url_prefix='/worker')
    
    # Home route
    @app.route('/')
    def index():
        if current_user.is_authenticated:
            if current_user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif current_user.role == 'employer':
                return redirect(url_for('employer.dashboard'))
            elif current_user.role == 'worker':
                return redirect(url_for('worker.dashboard'))
        return render_template('index.html')
    
    # Create database tables
    with app.app_context():
        db.create_all()
        # Create default admin if not exists
        create_default_admin()
    
    return app

def create_default_admin():
    """Create a default admin user if none exists"""
    from models import User, Admin
    
    admin_user = User.query.filter_by(email='admin@kaamdhandha.com').first()
    if not admin_user:
        admin_user = User(
            email='admin@kaamdhandha.com',
            role='admin'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        db.session.commit()
        
        admin_profile = Admin(
            user_id=admin_user.id,
            name='System Administrator',
            designation='Village Employment Officer'
        )
        db.session.add(admin_profile)
        db.session.commit()
        print('Default admin created: admin@kaamdhandha.com / admin123')

if __name__ == '__main__':
    app = create_app()
    # Use environment variable for debug mode
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
