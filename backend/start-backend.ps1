# E-Commerce Platform Backend Startup Script

Write-Host "🚀 Starting E-Commerce Backend..." -ForegroundColor Green

# Check if we're in the backend directory
if (-not (Test-Path ".\app\main.py")) {
    Write-Host "❌ Error: Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

# Check if virtual environment exists
if (-not (Test-Path ".\venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "🔧 Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Check if MongoDB is running (optional - just a warning)
Write-Host "⚠️  Make sure MongoDB is running on localhost:27017" -ForegroundColor Yellow

# Install/upgrade dependencies
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install -q --upgrade motor==3.4.0 pymongo==4.6.3 beanie==1.24.0 2>$null

# Check if .env exists
if (-not (Test-Path ".\.env")) {
    Write-Host "⚠️  Warning: .env file not found. Using default settings." -ForegroundColor Yellow
}

# Start the server
Write-Host "`n✨ Starting FastAPI server..." -ForegroundColor Green
Write-Host "📍 Backend API: http://localhost:8000" -ForegroundColor Cyan
Write-Host "📚 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "`nPress Ctrl+C to stop the server`n" -ForegroundColor Yellow

uvicorn app.main:app --reload
