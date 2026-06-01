from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Worker, Employer, Job, Application, EmploymentHistory, Admin
from functools import wraps
from sqlalchemy import func, extract
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # Statistics
    total_workers = Worker.query.count()
    total_employers = Employer.query.count()
    active_jobs = Job.query.filter_by(status='open').count()
    total_applications = Application.query.count()
    completed_jobs = Job.query.filter_by(status='completed').count()
    pending_employers = Employer.query.filter_by(approval_status='pending').count()
    
    # Recent activities
    recent_workers = Worker.query.order_by(Worker.created_at.desc()).limit(5).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()
    pending_employer_list = Employer.query.filter_by(approval_status='pending').limit(5).all()
    
    # Employment analytics - jobs by category
    jobs_by_category = db.session.query(
        Job.category, func.count(Job.id)
    ).group_by(Job.category).all()
    
    # Monthly employment trend
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    monthly_jobs = db.session.query(
        extract('month', Job.created_at).label('month'),
        func.count(Job.id)
    ).filter(Job.created_at >= six_months_ago).group_by('month').all()
    
    return render_template('admin/dashboard.html',
                         total_workers=total_workers,
                         total_employers=total_employers,
                         active_jobs=active_jobs,
                         total_applications=total_applications,
                         completed_jobs=completed_jobs,
                         pending_employers=pending_employers,
                         recent_workers=recent_workers,
                         recent_jobs=recent_jobs,
                         pending_employer_list=pending_employer_list,
                         jobs_by_category=jobs_by_category,
                         monthly_jobs=monthly_jobs)

@admin_bp.route('/workers')
@login_required
@admin_required
def workers():
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Worker.query
    if search:
        query = query.filter(
            (Worker.name.contains(search)) |
            (Worker.village.contains(search)) |
            (Worker.skills.contains(search))
        )
    
    workers = query.order_by(Worker.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/workers.html', workers=workers, search=search)

@admin_bp.route('/employers')
@login_required
@admin_required
def employers():
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Employer.query
    if status_filter != 'all':
        query = query.filter_by(approval_status=status_filter)
    
    employers = query.order_by(Employer.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/employers.html', employers=employers, status_filter=status_filter)

@admin_bp.route('/employer/approve/<int:employer_id>')
@login_required
@admin_required
def approve_employer(employer_id):
    employer = Employer.query.get_or_404(employer_id)
    employer.approval_status = 'approved'
    db.session.commit()
    flash(f'Employer {employer.name} has been approved.', 'success')
    return redirect(url_for('admin.employers'))

@admin_bp.route('/employer/reject/<int:employer_id>')
@login_required
@admin_required
def reject_employer(employer_id):
    employer = Employer.query.get_or_404(employer_id)
    employer.approval_status = 'rejected'
    db.session.commit()
    flash(f'Employer {employer.name} has been rejected.', 'warning')
    return redirect(url_for('admin.employers'))

@admin_bp.route('/jobs')
@login_required
@admin_required
def jobs():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category', 'all')
    status_filter = request.args.get('status', 'all')
    
    query = Job.query
    if category_filter != 'all':
        query = query.filter_by(category=category_filter)
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    jobs = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    from config import Config
    return render_template('admin/jobs.html', 
                         jobs=jobs, 
                         category_filter=category_filter,
                         status_filter=status_filter,
                         categories=Config.JOB_CATEGORIES)

@admin_bp.route('/reports')
@login_required
@admin_required
def reports():
    # Village-wise statistics
    village_stats = db.session.query(
        Worker.village,
        func.count(Worker.id).label('worker_count')
    ).group_by(Worker.village).all()
    
    # Top skilled workers
    top_workers = Worker.query.order_by(
        Worker.rating.desc(), 
        Worker.total_jobs_completed.desc()
    ).limit(10).all()
    
    # Top employers
    top_employers = Employer.query.filter_by(approval_status='approved').order_by(
        Employer.rating.desc()
    ).limit(10).all()
    
    # Total earnings by category
    earnings_by_category = db.session.query(
        Job.category,
        func.sum(EmploymentHistory.earning).label('total_earnings')
    ).join(EmploymentHistory).group_by(Job.category).all()
    
    return render_template('admin/reports.html',
                         village_stats=village_stats,
                         top_workers=top_workers,
                         top_employers=top_employers,
                         earnings_by_category=earnings_by_category)

@admin_bp.route('/user/toggle/<int:user_id>')
@login_required
@admin_required
def toggle_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'admin':
        flash('Cannot deactivate admin users.', 'danger')
        return redirect(request.referrer or url_for('admin.dashboard'))
    
    user.is_active = not user.is_active
    db.session.commit()
    
    status = 'activated' if user.is_active else 'deactivated'
    flash(f'User has been {status}.', 'success')
    return redirect(request.referrer or url_for('admin.dashboard'))
