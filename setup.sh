#!/bin/bash

# Twitter Task Manager - Setup Script
# This script sets up the complete Django application

set -e

echo "================================"
echo "Twitter Task Manager Setup"
echo "================================"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $python_version"
echo ""

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
    echo "Virtual environment created."
else
    echo "Virtual environment already exists."
fi

echo ""
echo "Activating virtual environment..."
source venv/Scripts/activate 2>/dev/null || source venv/bin/activate

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
echo "Dependencies installed."
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your Cloudinary credentials."
else
    echo "✓ .env file already exists."
fi

echo ""
echo "Running database migrations..."
python manage.py migrate
echo "✓ Database migrations completed."
echo ""

# Create superuser
echo "Creating superuser..."
echo "Please enter superuser credentials:"
python manage.py createsuperuser --noinput --username=admin --email=admin@example.com 2>/dev/null || {
    echo "Creating superuser with interactive prompt..."
    python manage.py createsuperuser
}
echo ""

echo "Collecting static files..."
python manage.py collectstatic --noinput
echo "✓ Static files collected."
echo ""

echo "================================"
echo "Setup Complete!"
echo "================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Cloudinary credentials"
echo "2. Run: python manage.py runserver"
echo "3. Visit: http://localhost:8000"
echo "4. Admin panel: http://localhost:8000/admin/"
echo ""
echo "Default admin credentials:"
echo "Username: admin"
echo "Email: admin@example.com"
echo ""
echo "First time setup:"
echo "1. Go to admin panel (/admin/)"
echo "2. Verify and create some posts"
echo "3. Sign up as a regular user"
echo "4. Verify the user in admin panel"
echo "5. Start claiming and completing posts"
echo ""
