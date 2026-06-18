@echo off
REM Twitter Task Manager - Windows Setup Script

echo.
echo ================================
echo Twitter Task Manager Setup
echo ================================
echo.

REM Check Python
python --version
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt
echo Dependencies installed.
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo .env file created. Please edit it with your Cloudinary credentials.
) else (
    echo .env file already exists.
)

echo.
echo Running database migrations...
python manage.py migrate
echo Database migrations completed.
echo.

echo Creating superuser...
python manage.py createsuperuser
echo.

echo Collecting static files...
python manage.py collectstatic --noinput
echo Static files collected.
echo.

echo.
echo ================================
echo Setup Complete!
echo ================================
echo.
echo Next steps:
echo 1. Edit .env file with your Cloudinary credentials
echo 2. Run: python manage.py runserver
echo 3. Visit: http://localhost:8000
echo 4. Admin panel: http://localhost:8000/admin/
echo.
pause
