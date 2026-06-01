# Installation Fix for Python 3.14

## Issue
Pillow 10.0.0 is not compatible with Python 3.14.

## Solution

### Step 1: Clean Up (if needed)
```bash
# Deactivate current venv if active
deactivate

# Remove old venv
rm -rf venv

# Navigate to gramconnect
cd gramconnect
```

### Step 2: Fresh Installation
```bash
# Create new virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies (Pillow removed as it's optional)
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

### Step 4: Access the Application
Open your browser and go to:
```
http://localhost:5000
```

## Default Login
- **Email:** admin@gramconnect.com
- **Password:** admin123

## Updated Requirements
The requirements.txt has been updated to:
- Remove Pillow (optional for image handling)
- Use compatible versions with Python 3.14
- Flask 3.0.0 and compatible packages

## If You Need Image Upload Support Later
```bash
pip install Pillow
```

## Quick Commands
```bash
# From the gramconnect directory:
source venv/bin/activate
python app.py
```

## Troubleshooting

### "Module not found" errors
Make sure venv is activated:
```bash
source venv/bin/activate
```

### Port already in use
Change port in app.py (last line):
```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database errors
Delete and recreate:
```bash
rm -rf database/village_jobs.db
python app.py
```
