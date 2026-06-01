# GramConnect - Rural Employment & Workforce Management Portal

## Vision
A digital platform inspired by NREGA and Apna Jobs that helps unemployed villagers find:
- Government jobs (NREGA works, Panchayat projects)
- Agricultural labor work
- Construction jobs
- Local shop and business jobs
- Skilled work (electrician, plumber, carpenter, tailor, driver)
- Daily wage opportunities

## Features

### For Workers
- Create profile with skills and experience
- Browse and search available jobs
- Apply for jobs with one click
- Track application status
- View earnings history
- Get job recommendations based on skills

### For Employers
- Post job opportunities
- View and manage applications
- Select workers for jobs
- Rate workers after job completion
- Track employment history

### For Admin (Village Employment Officer)
- Approve/reject employer registrations
- Monitor all workers and employers
- View employment analytics
- Generate village employment reports
- Manage platform users

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Jinja2 Templates
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

## Installation

1. **Clone the repository**
```bash
cd gramconnect
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
python app.py
```

5. **Access the application**
Open your browser and navigate to: `http://localhost:5000`

## Default Admin Credentials
- **Email**: admin@kaamdhandha.com
- **Password**: admin123

**Important**: Change the default admin password after first login!

## Project Structure
```
gramconnect/
│
├── app.py                 # Main application file
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
│
├── templates/             # HTML templates
│   ├── admin/            # Admin templates
│   ├── employer/         # Employer templates
│   ├── worker/           # Worker templates
│   └── auth/             # Authentication templates
│
├── static/               # Static files
│   ├── css/             # Stylesheets
│   ├── js/              # JavaScript files
│   └── uploads/         # User uploads
│
├── routes/               # Route handlers
│   ├── admin.py         # Admin routes
│   ├── employer.py      # Employer routes
│   ├── worker.py        # Worker routes
│   └── auth.py          # Authentication routes
│
├── database/             # SQLite database
│   └── village_jobs.db
│
└── reports/              # Generated reports
```

## Database Schema

### Users Table
- id, email, password_hash, role, is_active, created_at

### Workers Table
- id, user_id, name, mobile, village, skills, education, experience, rating, total_jobs_completed

### Employers Table
- id, user_id, name, business_type, contact, village, approval_status, rating

### Jobs Table
- id, employer_id, title, description, category, required_skills, wage, location, village, status

### Applications Table
- id, worker_id, job_id, status, applied_date, message

### Employment History Table
- id, worker_id, job_id, employer_id, earning, completion_date, ratings

## Job Categories
1. **Agriculture**: Harvesting, Planting, Irrigation, Dairy Farm Work
2. **Construction**: Mason, Painter, Labor Helper, Carpenter
3. **Services**: Electrician, Plumber, Driver, Housekeeping
4. **Local Business**: Shop Assistant, Delivery Partner, Warehouse Helper
5. **Government Works**: Road Construction, Water Conservation, Plantation Projects

## Key Features Implementation

### Role-Based Access Control
- Admin: Full system access
- Employer: Job posting and worker management (requires approval)
- Worker: Job browsing and application

### Employer Approval System
- New employers must be approved by admin
- Prevents fraudulent job postings
- Maintains platform quality

### Job Application Workflow
1. Worker browses available jobs
2. Worker applies with optional message
3. Employer reviews applications
4. Employer accepts/rejects applications
5. Job completion and rating

### Analytics & Reporting
- Village-wise employment statistics
- Category-wise job distribution
- Worker and employer ratings
- Earnings tracking

## Future Enhancements
- SMS/WhatsApp notifications
- Multi-language support (Hindi, Tamil, etc.)
- AI-based job recommendations
- Skill certification uploads
- Mobile app development
- Payment integration
- Geolocation-based job search

## Social Impact
This platform addresses:
- Rural unemployment
- Skill-job mismatch
- Lack of job visibility in villages
- Inefficient worker-employer matching
- Transparent wage tracking
- Digital inclusion in rural areas

## 🚀 Deployment

Kaam Dhandha is ready to deploy to the cloud! We've configured everything for you.

### Quick Deploy to Render (5 Minutes)

1. **Push to GitHub**
   ```bash
   cd gramconnect
   git init
   git add .
   git commit -m "Deploy Kaam Dhandha"
   git remote add origin YOUR_GITHUB_URL
   git push -u origin main
   ```

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Use these settings:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Add environment variable: `SECRET_KEY=your-random-key`
   - Click "Create Web Service"

3. **Done!** Your app will be live in 2-3 minutes at `https://kaamdhandha.onrender.com`

### Deployment Documentation

- **Quick Guide**: See `QUICK_DEPLOY.md` for 5-minute deployment
- **Full Guide**: See `DEPLOYMENT.md` for all platforms (Render, Railway, Heroku, etc.)
- **Checklist**: See `DEPLOY_CHECKLIST.md` for pre/post deployment tasks
- **Helper Script**: Run `./deploy.sh` for interactive deployment

### Supported Platforms

- ✅ **Render** (Recommended - Free tier)
- ✅ **Railway** (Fast & modern)
- ✅ **Heroku** (Classic & reliable)
- ✅ **PythonAnywhere** (Beginner-friendly)
- ✅ **Vercel** (Serverless)

---

## License
This project is created for educational purposes as part of IIT Madras coursework.

## Contact
For questions or support, contact the Village Employment Officer.
