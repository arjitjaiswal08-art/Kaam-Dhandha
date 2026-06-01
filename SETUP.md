# GramConnect - Quick Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

## Installation Steps

### 1. Navigate to Project Directory
```bash
cd gramconnect
```

### 2. Create Virtual Environment
```bash
python3 -m venv venv
```

### 3. Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Run the Application
```bash
python app.py
```

### 6. Access the Application
Open your web browser and go to:
```
http://localhost:5000
```

## Default Admin Login
- **Email:** admin@gramconnect.com
- **Password:** admin123

**⚠️ Important:** Change the admin password immediately after first login!

## Testing the Application

### 1. Login as Admin
- Use the default credentials above
- Explore the admin dashboard
- View workers, employers, jobs, and reports

### 2. Register as Worker
- Click "Register as Worker"
- Fill in your details and select skills
- Login and browse available jobs

### 3. Register as Employer
- Click "Register as Employer"
- Fill in business details
- Wait for admin approval (login as admin to approve)
- Post jobs after approval

### 4. Complete Workflow
1. Admin approves employer
2. Employer posts a job
3. Worker applies for the job
4. Employer reviews and accepts application
5. Employer marks job as completed

## Project Structure
```
gramconnect/
├── app.py                  # Main Flask application
├── config.py               # Configuration settings
├── models.py               # Database models
├── requirements.txt        # Python dependencies
├── routes/                 # Route handlers
│   ├── admin.py
│   ├── auth.py
│   ├── employer.py
│   └── worker.py
├── templates/              # HTML templates
│   ├── admin/
│   ├── auth/
│   ├── employer/
│   └── worker/
├── static/                 # Static files (CSS, JS, uploads)
└── database/               # SQLite database (auto-created)
```

## Features Implemented

### Admin Features
✅ Dashboard with statistics
✅ Manage workers
✅ Approve/reject employers
✅ View all jobs
✅ Generate reports and analytics
✅ User management

### Employer Features
✅ Post job opportunities
✅ View and manage applications
✅ Accept/reject worker applications
✅ Mark jobs as completed
✅ Profile management

### Worker Features
✅ Browse available jobs
✅ Apply for jobs
✅ Track application status
✅ View earnings history
✅ Profile with skills

## Database
- SQLite database is automatically created on first run
- Location: `database/village_jobs.db`
- No manual database setup required

## Troubleshooting

### Port Already in Use
If port 5000 is already in use, modify `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Change port
```

### Module Not Found Error
Make sure virtual environment is activated and dependencies are installed:
```bash
pip install -r requirements.txt
```

### Database Errors
Delete the database and restart:
```bash
rm -rf database/village_jobs.db
python app.py
```

## Next Steps
1. Customize the styling in `static/css/style.css`
2. Add more job categories in `config.py`
3. Implement SMS/WhatsApp notifications
4. Add multi-language support
5. Deploy to production server

## Support
For issues or questions, refer to README.md or contact the development team.
