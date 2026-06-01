# 📋 Deployment Checklist

## ✅ Pre-Deployment

- [ ] Test application locally
- [ ] All features working
- [ ] No errors in console
- [ ] Database migrations tested
- [ ] Requirements.txt updated
- [ ] .gitignore configured
- [ ] Remove sensitive data from code

## ✅ Git Setup

```bash
cd gramconnect
git init
git add .
git commit -m "Initial deployment"
```

## ✅ GitHub Push

```bash
# Create repository on GitHub first
git remote add origin https://github.com/YOUR_USERNAME/gramconnect.git
git push -u origin main
```

## ✅ Platform Selection

Choose one:
- [ ] **Render** (Recommended - Free, Easy)
- [ ] **Railway** (Fast, Modern)
- [ ] **Heroku** (Classic, Reliable)
- [ ] **PythonAnywhere** (Beginner-Friendly)
- [ ] **Vercel** (Serverless)

## ✅ Render Deployment (Recommended)

1. [ ] Go to https://render.com
2. [ ] Sign up / Login with GitHub
3. [ ] Click "New +" → "Web Service"
4. [ ] Connect gramconnect repository
5. [ ] Configure:
   - Name: `gramconnect`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Instance Type: `Free`
6. [ ] Add Environment Variable:
   - Key: `SECRET_KEY`
   - Value: (generate random key)
7. [ ] Click "Create Web Service"
8. [ ] Wait 2-3 minutes for deployment

## ✅ Post-Deployment

- [ ] App is accessible at provided URL
- [ ] Can login with admin credentials
- [ ] Change default admin password
- [ ] Test worker registration
- [ ] Test employer registration
- [ ] Test job posting
- [ ] Test job application
- [ ] Check mobile responsiveness
- [ ] Verify all pages load correctly

## ✅ Security

- [ ] Change SECRET_KEY to random value
- [ ] Change default admin password
- [ ] Remove debug mode in production
- [ ] Enable HTTPS (automatic on most platforms)
- [ ] Set up CORS if needed
- [ ] Review exposed endpoints

## ✅ Optional Enhancements

- [ ] Add custom domain
- [ ] Set up PostgreSQL database
- [ ] Configure email service
- [ ] Add error monitoring (Sentry)
- [ ] Set up analytics
- [ ] Configure backups
- [ ] Add rate limiting
- [ ] Set up CI/CD pipeline

## ✅ Documentation

- [ ] Update README with deployment URL
- [ ] Document environment variables
- [ ] Add API documentation (if applicable)
- [ ] Create user guide
- [ ] Add troubleshooting section

## ✅ Monitoring

- [ ] Check application logs
- [ ] Monitor error rates
- [ ] Track response times
- [ ] Set up uptime monitoring
- [ ] Configure alerts

## 🎯 Quick Commands

### Generate Secret Key
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

### Check Logs (Render)
- Go to dashboard → Logs tab

### Check Logs (Heroku)
```bash
heroku logs --tail
```

### Restart App (Render)
- Go to dashboard → Manual Deploy → Deploy

### Restart App (Heroku)
```bash
heroku restart
```

## 📱 Share Your App

Once deployed, your app will be at:
- **Render**: `https://gramconnect.onrender.com`
- **Railway**: `https://gramconnect.up.railway.app`
- **Heroku**: `https://gramconnect-app.herokuapp.com`

## 🆘 Troubleshooting

### Build Failed
- Check requirements.txt
- Verify Python version in runtime.txt
- Check build logs for errors

### App Crashes
- Check application logs
- Verify environment variables
- Test database connection

### Static Files Not Loading
- Check static file configuration
- Verify file paths
- Check CORS settings

### Database Errors
- Verify DATABASE_URL
- Check database migrations
- Ensure instance folder exists

## ✨ Success!

Your GramConnect app is now live and ready to use!

**Default Login:**
- Email: admin@gramconnect.com
- Password: admin123

**⚠️ CHANGE THE PASSWORD IMMEDIATELY!**

---

**Deployment URL**: ___________________________

**Deployed On**: ___________________________

**Notes**: ___________________________
