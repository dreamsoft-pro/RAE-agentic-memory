@echo off
title ScreenWatcher Backend Server
echo ===================================================
echo   ScreenWatcher - Native Windows Starter
echo ===================================================

cd /d %~dp0

:: Check if venv exists
if not exist "venv" (
    echo [ERROR] Virtual environment 'venv' not found!
    echo Please create it first using: python -m venv venv
    pause
    exit /b
)

echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo [2/3] Checking dependencies...
pip install -r requirements.txt --quiet

echo [3/3] Preparing database...
python manage.py migrate
python manage.py collectstatic --noinput

echo ---------------------------------------------------
echo SERVER STARTING AT http://127.0.0.1:8000
echo Press Ctrl+C to stop
echo ---------------------------------------------------
python manage.py runserver 0.0.0.0:8000

pause
