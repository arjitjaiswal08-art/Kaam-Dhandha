# GramConnect - Deployment Guide

## 🚀 Quick Deployment Options

### Option 1: Render (Recommended - Free Tier Available)

**Steps:**

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Push to GitHub**
   ```bash
   cd gramconnect
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

3. **Deploy on Render**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: gramconnect
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `gunicorn app:app`
     - **Instance Type**: Free

4. **Add Environment Variables**
   - Go to "Environment" tab
   - Add:
     ```
     SECRET_KEY=your-secret-key-here-change-this
     DATABASE_URL=sqlite:///village_jobs.db
     ```

5. **Deploy!**
   - Click "Create Web Service"
   - Wait 2-3 minutes
   - Your app will be live at: `https://gramconnect.onrender.com`

---

### Option 2: Railway (Easy & Fast)

**Steps:**

1. **Install Railway CLI** (Optional)
   ```bash
   npm install -g @railway/cli
   ```

2. **Deploy via GitHub**
   - Go to https://railway.app
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your gramconnect repository
   - Railway auto-detects Python and deploys!

3. **Environment Variables**
   - Add in Railway dashboard:
     ```
     SECRET_KEY=your-secret-key-here
     ```

4. **Access Your App**
   - Railway provides a URL automatically
   - Example: `https://gramconnect-production.up.railway.app`

---

### Option 3: Heroku (Classic Option)

**Steps:**

1. **Install Heroku CLI**
   ```bash
   brew install heroku/brew/heroku  # macOS
   ```

2. **Login and Create App**
   ```bash
   cd gramconnect
   heroku login
   heroku create gramconnect-app
   ```

3. **Deploy**
   ```bash
   git init
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set SECRET_KEY=your-secret-key-here
   ```

5. **Open App**
   ```bash
   heroku open
   ```

---

### Option 4: PythonAnywhere (Good for Beginners)

**Steps:**

1. **Create Account**
   - Go to https://www.pythonanywhere.com
   - Sign up for free account

2. **Upload Files**
   - Go to "Files" tab
   - Upload your gramconnect folder
   - Or use Git:
     ```bash
     git clone YOUR_GITHUB_REPO_URL
     ```

3. **Create Virtual Environment**
   ```bash
   cd gramconnect
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Web App**
   - Go to "Web" tab
   - Click "Add a new web app"
   - Choose "Manual configuration"
   - Python 3.10
   - Set source code: `/home/yourusername/gramconnect`
   - Set virtualenv: `/home/yourusername/gramconnect/venv`

5. **Edit WSGI File**
   ```python
   import sys
   path = '/home/yourusername/gramconnect'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

6. **Reload Web App**
   - Click "Reload" button
   - Access at: `https://yourusername.pythonanywhere.com`

---

### Option 5: Vercel (Serverless)

**Steps:**

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Create vercel.json**
   Already created in your project!

3. **Deploy**
   ```bash
   cd gramconnect
   vercel
   ```

4. **Follow Prompts**
   - Link to existing project or create new
   - Deploy!

---

## 🔒 Production Configuration

### 1. Change Secret Key

**Generate a secure secret key:**
```python
import secrets
print(secrets.token_hex(32))
```

Set it as environment variable:
```bash
export SECRET_KEY=your-generated-key
```

### 2. Use PostgreSQL (Recommended for Production)

**Update config.py:**
```python
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///village_jobs.db'

# Fix for Heroku PostgreSQL URL
if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
```

### 3. Disable Debug Mode

**In app.py:**
```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=False)  # Set to False in production
```

### 4. Set Up HTTPS

Most platforms (Render, Railway, Heroku) provide HTTPS automatically!

---

## 📊 Database Migration (SQLite to PostgreSQL)

If you want to migrate from SQLite to PostgreSQL:

1. **Export SQLite Data**
   ```bash
   sqlite3 instance/village_jobs.db .dump > backup.sql
   ```

2. **Create PostgreSQL Database**
   - On Render: Automatically provided
   - On Heroku: `heroku addons:create heroku-postgresql:mini`

3. **Update DATABASE_URL**
   ```bash
   export DATABASE_URL=postgresql://user:pass@host:5432/dbname
   ```

4. **Run Migrations**
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app()
   >>> with app.app_context():
   ...     db.create_all()
   ```

---

## 🔧 Troubleshooting

### Issue: "Application Error"
**Solution:** Check logs
```bash
# Heroku
heroku logs --tail

# Render
Check "Logs" tab in dashboard
```

### Issue: Database not found
**Solution:** Ensure instance folder exists
```python
# In app.py
os.makedirs('instance', exist_ok=True)
```

### Issue: Static files not loading
**Solution:** Configure static files
```python
# In app.py
app.static_folder = 'static'
app.static_url_path = '/static'
```

---

## 🎯 Recommended: Render Deployment (Step-by-Step)

### 1. Prepare Repository
```bash
cd gramconnect
git init
git add .
git commit -m "Ready for deployment"
```

### 2. Push to GitHub
```bash
# Create repo on GitHub first
git remote add origin https://github.com/yourusername/gramconnect.git
git push -u origin main
```

### 3. Deploy on Render
1. Go to https://render.com/dashboard
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Fill in:
   - **Name**: gramconnect
   - **Branch**: main
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
5. Click "Create Web Service"

### 4. Wait for Deployment
- Takes 2-3 minutes
- Watch build logs
- App will be live at provided URL

### 5. Test Your App
- Visit the URL
- Login with: admin@gramconnect.com / admin123
- Change admin password immediately!

---

## 🌐 Custom Domain (Optional)

### On Render:
1. Go to "Settings" → "Custom Domain"
2. Add your domain
3. Update DNS records as shown

### On Railway:
1. Go to "Settings" → "Domains"
2. Add custom domain
3. Configure DNS

---

## 📱 Post-Deployment Checklist

- [ ] Change default admin password
- [ ] Set strong SECRET_KEY
- [ ] Test all features
- [ ] Check mobile responsiveness
- [ ] Set up error monitoring (Sentry)
- [ ] Configure backups
- [ ] Add custom domain (optional)
- [ ] Set up SSL certificate (usually automatic)
- [ ] Test email functionality (if added)
- [ ] Monitor performance

---

## 🎉 Your App is Live!

Share your deployment URL:
- **Render**: `https://gramconnect.onrender.com`
- **Railway**: `https://gramconnect.up.railway.app`
- **Heroku**: `https://gramconnect-app.herokuapp.com`
- **PythonAnywhere**: `https://yourusername.pythonanywhere.com`

---

## 💡 Tips

1. **Free Tier Limitations:**
   - Render: Spins down after 15 min inactivity
   - Railway: 500 hours/month free
   - Heroku: Requires credit card for free tier
   - PythonAnywhere: Limited CPU time

2. **Keep App Awake:**
   - Use UptimeRobot to ping your app every 5 minutes
   - Prevents spin-down on free tiers

3. **Monitoring:**
   - Set up error tracking with Sentry
   - Use platform's built-in monitoring

4. **Backups:**
   - Export database regularly
   - Keep code in GitHub

---

## 🆘 Need Help?

- Check platform documentation
- Review deployment logs
- Test locally first
- Ensure all files are committed to Git

**Good luck with your deployment! 🚀**
