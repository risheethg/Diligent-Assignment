@echo off
echo Starting E-Commerce Backend...
cd /d "%~dp0"

if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing/upgrading dependencies...
pip install -q --upgrade motor==3.4.0 pymongo==4.6.3 beanie==1.24.0
pip install -q -r requirements.txt

echo.
echo ========================================
echo Backend API: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Starting FastAPI server...
echo Press Ctrl+C to stop
echo.

venv\Scripts\python.exe -m uvicorn app.main:app --reload
