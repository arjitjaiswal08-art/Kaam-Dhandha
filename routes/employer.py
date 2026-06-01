from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db, Employer, Job, Application, Worker, EmploymentHistory
from functools import wraps
from datetime import datetime

employer_bp = Blueprint('employer', __name__)

def employer_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'employer':
            flash('Access denied. Employer privileges required.', 'danger')
            return redirect(url_for('index'))
        
        employer = Employer.query.filter_by(user_id=current_user.id).first()
        if employer and employer.approval_status != 'approved':
            flash('Your account is pending approval.', 'warning')
            return render_template('employer/pending_approval.html')
        
        return f(*args, **kwargs)
    return decorated_function

@employer_bp.route('/dashboard')
@login_required
@employer_required
def dashboard():
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    
    active_jobs = Job.query.filter_by(employer_id=employer.id, status='open').count()
    total_applications = Application.query.join(Job).filter(Job.employer_id == employer.id).count()
    completed_jobs = Job.query.filter_by(employer_id=employer.id, status='completed').count()
    
    recent_jobs = Job.query.filter_by(employer_id=employer.id).order_by(Job.created_at.desc()).limit(5).all()
    recent_applications = Application.query.join(Job).filter(
        Job.employer_id == employer.id
    ).order_by(Application.applied_date.desc()).limit(5).all()
    
    return render_template('employer/dashboard.html',
                         employer=employer,
                         active_jobs=active_jobs,
                         total_applications=total_applications,
                         completed_jobs=completed_jobs,
                         recent_jobs=recent_jobs,
                         recent_applications=recent_applications)

@employer_bp.route('/jobs')
@login_required
@employer_required
def jobs():
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    
    query = Job.query.filter_by(employer_id=employer.id)
    
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    jobs = query.order_by(Job.created_at.desc()).paginate(
        page=page, per_page=10, error_out=False
    )
    
    return render_template('employer/jobs.html', jobs=jobs, status_filter=status_filter)

@employer_bp.route('/job/create', methods=['GET', 'POST'])
@login_required
@employer_required
def create_job():
    if request.method == 'POST':
        employer = Employer.query.filter_by(user_id=current_user.id).first()
        
        job = Job(
            employer_id=employer.id,
            title=request.form.get('title'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            required_skills=','.join(request.form.getlist('required_skills')),
            wage=float(request.form.get('wage')),
            wage_type=request.form.get('wage_type'),
            location=request.form.get('location'),
            village=request.form.get('village'),
            vacancies=int(request.form.get('vacancies', 1)),
            deadline=datetime.strptime(request.form.get('deadline'), '%Y-%m-%d').date() if request.form.get('deadline') else None
        )
        
        db.session.add(job)
        db.session.commit()
        
        flash('Job posted successfully!', 'success')
        return redirect(url_for('employer.jobs'))
    
    from config import Config
    return render_template('employer/create_job.html', 
                         categories=Config.JOB_CATEGORIES,
                         skills_list=Config.SKILLS_LIST)

@employer_bp.route('/job/<int:job_id>')
@login_required
@employer_required
def view_job(job_id):
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    job = Job.query.filter_by(id=job_id, employer_id=employer.id).first_or_404()
    
    applications = Application.query.filter_by(job_id=job.id).order_by(
        Application.applied_date.desc()
    ).all()
    
    return render_template('employer/view_job.html', job=job, applications=applications)

@employer_bp.route('/application/accept/<int:application_id>')
@login_required
@employer_required
def accept_application(application_id):
    application = Application.query.get_or_404(application_id)
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    
    if application.job.employer_id != employer.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('employer.dashboard'))
    
    application.status = 'accepted'
    db.session.commit()
    
    flash('Application accepted!', 'success')
    return redirect(url_for('employer.view_job', job_id=application.job_id))

@employer_bp.route('/application/reject/<int:application_id>')
@login_required
@employer_required
def reject_application(application_id):
    application = Application.query.get_or_404(application_id)
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    
    if application.job.employer_id != employer.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('employer.dashboard'))
    
    application.status = 'rejected'
    db.session.commit()
    
    flash('Application rejected.', 'info')
    return redirect(url_for('employer.view_job', job_id=application.job_id))

@employer_bp.route('/job/<int:job_id>/complete', methods=['POST'])
@login_required
@employer_required
def complete_job(job_id):
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    job = Job.query.filter_by(id=job_id, employer_id=employer.id).first_or_404()
    
    job.status = 'completed'
    db.session.commit()
    
    flash('Job marked as completed!', 'success')
    return redirect(url_for('employer.jobs'))

@employer_bp.route('/profile')
@login_required
@employer_required
def profile():
    employer = Employer.query.filter_by(user_id=current_user.id).first()
    return render_template('employer/profile.html', employer=employer)
