#!/bin/bash

echo "========================================="
echo "  GramConnect - Starting Application"
echo "========================================="
echo ""

# Deactivate any active environment
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivating current environment..."
    deactivate 2>/dev/null || true
fi

# Make sure we're in the gramconnect directory
cd "$(dirname "$0")"

# Create venv if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the venv
echo "Activating virtual environment..."
source venv/bin/activate

# Verify we're using the right Python
echo "Using Python: $(which python)"

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip --quiet
pip install -r requirements.txt

# Create database directory
mkdir -p database

echo ""
echo "========================================="
echo "  Application Starting"
echo "========================================="
echo ""
echo "Admin Login:"
echo "  Email: admin@gramconnect.com"
echo "  Password: admin123"
echo ""
echo "Open browser: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Run the app
python app.py
