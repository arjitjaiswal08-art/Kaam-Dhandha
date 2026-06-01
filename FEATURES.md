# GramConnect - Feature Documentation

## Core Features

### 1. Role-Based Access Control (RBAC)
Three distinct user roles with specific permissions:

#### Admin (Village Employment Officer)
- **Dashboard**: View comprehensive statistics
- **Worker Management**: View all registered workers, activate/deactivate accounts
- **Employer Management**: Approve/reject employer registrations
- **Job Oversight**: Monitor all job postings across the platform
- **Analytics**: Generate employment reports and village statistics
- **User Control**: Manage user accounts and permissions

#### Employer
- **Job Posting**: Create detailed job listings with requirements
- **Application Management**: Review worker applications
- **Worker Selection**: Accept or reject applicants
- **Job Tracking**: Monitor active, closed, and completed jobs
- **Profile Management**: Maintain business information
- **Approval System**: Account requires admin approval before posting jobs

#### Worker
- **Job Discovery**: Browse and search available opportunities
- **Application System**: Apply for jobs with optional messages
- **Status Tracking**: Monitor application progress
- **Earnings History**: View completed jobs and earnings
- **Profile Management**: Showcase skills and experience
- **Job Recommendations**: Get matched with relevant opportunities

### 2. Job Management System

#### Job Categories
1. **Agriculture**
   - Harvesting
   - Planting
   - Irrigation
   - Dairy Farm Work

2. **Construction**
   - Mason
   - Painter
   - Labor Helper
   - Carpenter

3. **Services**
   - Electrician
   - Plumber
   - Driver
   - Housekeeping

4. **Local Business**
   - Shop Assistant
   - Delivery Partner
   - Warehouse Helper

5. **Government Works**
   - Road Construction
   - Water Conservation
   - Plantation Projects
   - Panchayat Development

#### Job Attributes
- Title and detailed description
- Category classification
- Required skills
- Wage amount and type (daily/weekly/monthly/per task)
- Location and village
- Number of vacancies
- Application deadline
- Status (open/closed/completed)

### 3. Application Workflow

```
Worker applies → Employer reviews → Accept/Reject → Job completion → Rating
```

1. **Application Submission**
   - Worker browses jobs
   - Applies with optional message
   - Cannot apply twice to same job

2. **Employer Review**
   - View all applications
   - See worker profiles and ratings
   - Accept or reject applications

3. **Job Completion**
   - Employer marks job as completed
   - Records added to employment history
   - Earnings tracked for workers

4. **Rating System**
   - Workers rated by employers
   - Employers rated by workers
   - Ratings influence future opportunities

### 4. Search and Filter

#### Worker Job Search
- Filter by category
- Filter by village/location
- Keyword search in title/description
- Pagination for large result sets

#### Admin Filters
- Workers by name, village, skills
- Employers by approval status
- Jobs by category and status

### 5. Analytics and Reporting

#### Admin Dashboard Statistics
- Total workers registered
- Total employers (with pending count)
- Active jobs count
- Total applications
- Completed jobs

#### Reports
- **Village-wise Distribution**: Worker count per village
- **Top Workers**: Highest rated and most jobs completed
- **Top Employers**: Best rated employers
- **Earnings by Category**: Total wages paid per job category
- **Monthly Trends**: Job posting trends over time

### 6. Security Features

#### Authentication
- Email and password-based login
- Password hashing using Werkzeug
- Session management with Flask-Login
- Remember me functionality

#### Authorization
- Role-based route protection
- Decorator-based access control
- Employer approval system
- User activation/deactivation

#### Data Validation
- Form validation
- Duplicate application prevention
- Unique email enforcement
- Required field validation

### 7. User Experience

#### Responsive Design
- Bootstrap 5 framework
- Mobile-friendly interface
- Card-based layouts
- Intuitive navigation

#### Visual Feedback
- Flash messages for actions
- Status badges (pending/accepted/rejected)
- Color-coded statistics
- Icon-based navigation

#### Pagination
- 10 jobs per page
- 20 workers/employers per page
- Page navigation controls
- Current page highlighting

### 8. Database Schema

#### Users Table
- Authentication credentials
- Role assignment
- Account status

#### Workers Table
- Personal information
- Skills and experience
- Rating and job count
- Village location

#### Employers Table
- Business information
- Approval status
- Contact details
- Rating

#### Jobs Table
- Job details
- Wage information
- Location and requirements
- Status tracking

#### Applications Table
- Worker-job relationship
- Application status
- Timestamps
- Optional messages

#### Employment History Table
- Completed jobs record
- Earnings tracking
- Ratings (bidirectional)
- Completion dates

## Advanced Features (Implemented)

### 1. Profile Completion Tracking
- Workers can see their profile status
- Skills showcase
- Experience display
- Rating visibility

### 2. Job Status Management
- Open: Accepting applications
- Closed: No longer accepting
- Completed: Job finished

### 3. Employer Approval Workflow
- New employers start as "pending"
- Admin reviews and approves/rejects
- Approved employers can post jobs
- Rejected employers cannot access features

### 4. Application Status Tracking
- Pending: Awaiting employer review
- Accepted: Worker selected for job
- Rejected: Application declined

## Future Enhancement Opportunities

### Phase 2 Features
1. **SMS/WhatsApp Notifications**
   - Job alerts
   - Application status updates
   - Deadline reminders

2. **Multi-language Support**
   - Hindi, Tamil, Telugu, etc.
   - Language switcher
   - Localized content

3. **Advanced Search**
   - Geolocation-based job search
   - Salary range filters
   - Date range filters

4. **Skill Certification**
   - Upload certificates
   - Skill verification
   - Training recommendations

5. **Payment Integration**
   - Online wage payments
   - Payment history
   - Invoice generation

6. **Mobile Application**
   - Native iOS/Android apps
   - Push notifications
   - Offline mode

7. **AI Recommendations**
   - Job matching algorithm
   - Skill gap analysis
   - Career path suggestions

8. **Video Profiles**
   - Worker introduction videos
   - Skill demonstrations
   - Employer testimonials

9. **Chat System**
   - Direct messaging
   - Group discussions
   - File sharing

10. **Advanced Analytics**
    - Predictive analytics
    - Employment trends
    - Skill demand forecasting

## Technical Specifications

### Technology Stack
- **Backend**: Flask 2.3.3
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: Bootstrap 5, Jinja2
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF

### Performance
- Lightweight SQLite database
- Efficient query optimization
- Pagination for large datasets
- Minimal external dependencies

### Scalability
- Modular architecture
- Blueprint-based routing
- Configurable settings
- Easy database migration path

### Maintainability
- Clean code structure
- Comprehensive comments
- Separation of concerns
- RESTful route design
