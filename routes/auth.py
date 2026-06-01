from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Worker, Employer
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('Your account has been deactivated. Please contact admin.', 'danger')
                return redirect(url_for('auth.login'))
            
            login_user(user, remember=True)
            next_page = request.args.get('next')
            
            if next_page:
                return redirect(next_page)
            
            # Redirect based on role
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard'))
            elif user.role == 'employer':
                return redirect(url_for('employer.dashboard'))
            elif user.role == 'worker':
                return redirect(url_for('worker.dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/register/worker', methods=['GET', 'POST'])
def register_worker():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        mobile = request.form.get('mobile')
        village = request.form.get('village')
        skills = request.form.getlist('skills')
        education = request.form.get('education')
        experience = request.form.get('experience', 0)
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register_worker'))
        
        # Create user
        user = User(email=email, role='worker')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create worker profile
        worker = Worker(
            user_id=user.id,
            name=name,
            mobile=mobile,
            village=village,
            skills=','.join(skills),
            education=education,
            experience=int(experience) if experience else 0
        )
        db.session.add(worker)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('auth.login'))
    
    from config import Config
    return render_template('auth/register_worker.html', skills_list=Config.SKILLS_LIST)

@auth_bp.route('/register/employer', methods=['GET', 'POST'])
def register_employer():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        name = request.form.get('name')
        business_type = request.form.get('business_type')
        contact = request.form.get('contact')
        village = request.form.get('village')
        address = request.form.get('address')
        
        # Check if user exists
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('auth.register_employer'))
        
        # Create user
        user = User(email=email, role='employer')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        # Create employer profile
        employer = Employer(
            user_id=user.id,
            name=name,
            business_type=business_type,
            contact=contact,
            village=village,
            address=address,
            approval_status='pending'
        )
        db.session.add(employer)
        db.session.commit()
        
        flash('Registration successful! Your account is pending approval.', 'info')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register_employer.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))
