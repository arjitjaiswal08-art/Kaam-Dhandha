from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Worker, Job, Application, EmploymentHistory
from functools import wraps
from sqlalchemy import or_

worker_bp = Blueprint('worker', __name__)

def worker_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'worker':
            flash('Access denied. Worker privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@worker_bp.route('/dashboard')
@login_required
@worker_required
def dashboard():
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    
    available_jobs = Job.query.filter_by(status='open').count()
    my_applications = Application.query.filter_by(worker_id=worker.id).count()
    accepted_applications = Application.query.filter_by(
        worker_id=worker.id, status='accepted'
    ).count()
    
    total_earnings = db.session.query(db.func.sum(EmploymentHistory.earning)).filter_by(
        worker_id=worker.id
    ).scalar() or 0
    
    recent_jobs = Job.query.filter_by(status='open').order_by(
        Job.created_at.desc()
    ).limit(5).all()
    
    my_recent_applications = Application.query.filter_by(
        worker_id=worker.id
    ).order_by(Application.applied_date.desc()).limit(5).all()
    
    return render_template('worker/dashboard.html',
                         worker=worker,
                         available_jobs=available_jobs,
                         my_applications=my_applications,
                         accepted_applications=accepted_applications,
                         total_earnings=total_earnings,
                         recent_jobs=recent_jobs,
                         my_recent_applications=my_recent_applications)

@worker_bp.route('/jobs')
@login_required
@worker_required
def jobs():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', 'all')
    village = request.args.get('village', '')
    search = request.args.get('search', '')
    
    query = Job.query.filter_by(status='open')
    
    if category != 'all':
        query = query.filter_by(category=category)
    
    if village:
        query = query.filter_by(village=village)
    
    if search:
        query = query.filter(
            or_(
                Job.title.contains(search),
                Job.description.contains(search),
                Job.required_skills.contains(search)
            )
        )
    
    jobs = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    from config import Config
    return render_template('worker/jobs.html', 
                         jobs=jobs, 
                         category=category,
                         village=village,
                         search=search,
                         categories=Config.JOB_CATEGORIES)

@worker_bp.route('/job/<int:job_id>')
@login_required
@worker_required
def view_job(job_id):
    job = Job.query.get_or_404(job_id)
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    
    # Check if already applied
    existing_application = Application.query.filter_by(
        worker_id=worker.id, job_id=job.id
    ).first()
    
    return render_template('worker/view_job.html', 
                         job=job, 
                         existing_application=existing_application)

@worker_bp.route('/job/<int:job_id>/apply', methods=['POST'])
@login_required
@worker_required
def apply_job(job_id):
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    job = Job.query.get_or_404(job_id)
    
    # Check if already applied
    existing = Application.query.filter_by(worker_id=worker.id, job_id=job.id).first()
    if existing:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('worker.view_job', job_id=job_id))
    
    application = Application(
        worker_id=worker.id,
        job_id=job.id,
        message=request.form.get('message', '')
    )
    
    db.session.add(application)
    db.session.commit()
    
    flash('Application submitted successfully!', 'success')
    return redirect(url_for('worker.my_applications'))

@worker_bp.route('/applications')
@login_required
@worker_required
def my_applications():
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Application.query.filter_by(worker_id=worker.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    applications = query.order_by(Application.applied_date.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('worker/applications.html', 
                         applications=applications,
                         status_filter=status_filter)

@worker_bp.route('/earnings')
@login_required
@worker_required
def earnings():
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    
    history = EmploymentHistory.query.filter_by(worker_id=worker.id).order_by(
        EmploymentHistory.completion_date.desc()
    ).all()
    
    total_earnings = db.session.query(db.func.sum(EmploymentHistory.earning)).filter_by(
        worker_id=worker.id
    ).scalar() or 0
    
    return render_template('worker/earnings.html', 
                         history=history,
                         total_earnings=total_earnings)

@worker_bp.route('/profile')
@login_required
@worker_required
def profile():
    worker = Worker.query.filter_by(user_id=current_user.id).first()
    return render_template('worker/profile.html', worker=worker)
