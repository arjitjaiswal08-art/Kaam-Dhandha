#!/bin/bash

echo "========================================="
echo "  GramConnect - Deployment Helper"
echo "========================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit for deployment"
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

echo ""
echo "========================================="
echo "  Deployment Options"
echo "========================================="
echo ""
echo "1. Render (Recommended - Free)"
echo "2. Railway (Fast & Modern)"
echo "3. Heroku (Classic)"
echo "4. Manual GitHub Push"
echo ""
read -p "Choose option (1-4): " choice

case $choice in
    1)
        echo ""
        echo "📦 Preparing for Render deployment..."
        echo ""
        echo "Steps to deploy on Render:"
        echo "1. Push code to GitHub (option 4)"
        echo "2. Go to https://render.com"
        echo "3. Click 'New +' → 'Web Service'"
        echo "4. Connect your GitHub repository"
        echo "5. Use these settings:"
        echo "   - Build Command: pip install -r requirements.txt"
        echo "   - Start Command: gunicorn app:app"
        echo "6. Add environment variable:"
        echo "   - SECRET_KEY: $(python3 -c 'import secrets; print(secrets.token_hex(32))')"
        echo ""
        echo "✓ Ready for Render deployment!"
        ;;
    2)
        echo ""
        echo "🚂 Preparing for Railway deployment..."
        echo ""
        echo "Steps to deploy on Railway:"
        echo "1. Push code to GitHub (option 4)"
        echo "2. Go to https://railway.app"
        echo "3. Click 'Start a New Project'"
        echo "4. Select 'Deploy from GitHub repo'"
        echo "5. Choose your gramconnect repository"
        echo "6. Railway will auto-detect and deploy!"
        echo ""
        echo "✓ Ready for Railway deployment!"
        ;;
    3)
        echo ""
        echo "🟣 Preparing for Heroku deployment..."
        echo ""
        if command -v heroku &> /dev/null; then
            echo "Heroku CLI found!"
            read -p "Enter app name (e.g., gramconnect-app): " appname
            heroku create $appname
            echo "Generating secret key..."
            SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
            heroku config:set SECRET_KEY=$SECRET_KEY
            echo ""
            echo "Ready to deploy! Run:"
            echo "  git push heroku main"
        else
            echo "Heroku CLI not found. Install it first:"
            echo "  brew install heroku/brew/heroku"
        fi
        ;;
    4)
        echo ""
        echo "📤 Pushing to GitHub..."
        echo ""
        read -p "Enter your GitHub repository URL: " repo_url
        
        if git remote | grep -q "origin"; then
            echo "Remote 'origin' already exists. Updating..."
            git remote set-url origin $repo_url
        else
            git remote add origin $repo_url
        fi
        
        git add .
        git commit -m "Ready for deployment" || echo "No changes to commit"
        git branch -M main
        git push -u origin main
        
        echo ""
        echo "✓ Code pushed to GitHub!"
        echo ""
        echo "Next steps:"
        echo "1. Go to your deployment platform (Render/Railway/Heroku)"
        echo "2. Connect your GitHub repository"
        echo "3. Deploy!"
        ;;
    *)
        echo "Invalid option"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "  Deployment Information"
echo "========================================="
echo ""
echo "📄 Files created:"
echo "  ✓ Procfile (for Heroku)"
echo "  ✓ runtime.txt (Python version)"
echo "  ✓ requirements.txt (dependencies)"
echo "  ✓ vercel.json (for Vercel)"
echo ""
echo "📚 Documentation:"
echo "  ✓ DEPLOYMENT.md (full guide)"
echo "  ✓ QUICK_DEPLOY.md (5-minute guide)"
echo "  ✓ DEPLOY_CHECKLIST.md (checklist)"
echo ""
echo "🔑 Don't forget to:"
echo "  1. Set SECRET_KEY environment variable"
echo "  2. Change default admin password after deployment"
echo "  3. Test all features on production"
echo ""
echo "========================================="
echo "  Good luck with your deployment! 🚀"
echo "========================================="
