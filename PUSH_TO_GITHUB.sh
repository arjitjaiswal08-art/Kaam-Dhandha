#!/bin/bash

echo "========================================="
echo "  Pushing Kaam Dhandha to GitHub"
echo "========================================="
echo ""

# Initialize git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
    echo "✓ Git initialized"
else
    echo "✓ Git already initialized"
fi

# Add all files
echo ""
echo "Adding files..."
git add .

# Commit
echo ""
echo "Committing changes..."
git commit -m "Initial commit - Kaam Dhandha Rural Employment Portal"

# Set branch to main
echo ""
echo "Setting branch to main..."
git branch -M main

# Add remote (if not already added)
echo ""
echo "Adding remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/arjitjaiswal08-art/Kaam-Dhandha.git

# Push to GitHub
echo ""
echo "Pushing to GitHub..."
git push -u origin main

echo ""
echo "========================================="
echo "  ✓ Successfully pushed to GitHub!"
echo "========================================="
echo ""
echo "Your repository: https://github.com/arjitjaiswal08-art/Kaam-Dhandha"
echo ""
echo "Next steps:"
echo "1. Go to https://render.com"
echo "2. Deploy your app from GitHub"
echo "3. Your app will be live in minutes!"
echo ""
