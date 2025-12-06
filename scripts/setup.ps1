# Setup Script for Windows (PowerShell)
#
# This script sets up the development environment for The Wizard's Keep
#
# Educational Notes:
# - PowerShell is the modern shell for Windows
# - Error handling with try/catch ensures robust scripts
# - Functions organize code for reusability

# Set error handling
$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  The Wizard's Keep - Development Setup" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Function to check if command exists
function Test-Command {
    param($Command)
    try {
        if (Get-Command $Command -ErrorAction Stop) {
            return $true
        }
    }
    catch {
        return $false
    }
}

# Check prerequisites
Write-Host "Checking prerequisites..." -ForegroundColor Yellow

# Check Python
if (-not (Test-Command python)) {
    Write-Host "❌ Python is not installed. Please install Python 3.11 or higher." -ForegroundColor Red
    exit 1
}

$pythonVersion = python --version
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Check Docker
if (-not (Test-Command docker)) {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop or Rancher Desktop." -ForegroundColor Red
    exit 1
}

$dockerVersion = docker --version
Write-Host "✅ Found: $dockerVersion" -ForegroundColor Green

# Check Git
if (-not (Test-Command git)) {
    Write-Host "⚠️  Git is not installed. Git is recommended but optional." -ForegroundColor Yellow
}
else {
    $gitVersion = git --version
    Write-Host "✅ Found: $gitVersion" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setting up Python virtual environment..." -ForegroundColor Yellow

# Create virtual environment
if (Test-Path "venv") {
    Write-Host "Virtual environment already exists. Skipping creation." -ForegroundColor Yellow
}
else {
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install backend dependencies
Write-Host ""
Write-Host "Installing backend dependencies..." -ForegroundColor Yellow
Set-Location backend
pip install -r requirements-dev.txt
Set-Location ..
Write-Host "✅ Backend dependencies installed" -ForegroundColor Green

# Create .env file if it doesn't exist
Write-Host ""
Write-Host "Setting up environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.env")) {
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ Created .env file from .env.example" -ForegroundColor Green
    Write-Host "⚠️  Please review and update backend\.env with your settings" -ForegroundColor Yellow
}
else {
    Write-Host ".env file already exists. Skipping." -ForegroundColor Yellow
}

# Start database with Docker
Write-Host ""
Write-Host "Starting PostgreSQL database..." -ForegroundColor Yellow
docker run -d `
    --name wizards-keep-db `
    -p 5432:5432 `
    -e POSTGRES_USER=wizard `
    -e POSTGRES_PASSWORD=wizard123 `
    -e POSTGRES_DB=wizards_keep `
    postgres:15-alpine 2>$null

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database container started" -ForegroundColor Green
}
elseif ($LASTEXITCODE -eq 125) {
    Write-Host "⚠️  Database container already exists. Starting it..." -ForegroundColor Yellow
    docker start wizards-keep-db
}

# Wait for database to be ready
Write-Host "Waiting for database to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 3

# Initialize database
Write-Host ""
Write-Host "Initializing game database..." -ForegroundColor Yellow
Set-Location backend
python scripts\init_db.py
Set-Location ..
Write-Host "✅ Database initialized with game content" -ForegroundColor Green

Write-Host ""
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the application:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  1. Start the backend:" -ForegroundColor White
Write-Host "     cd backend" -ForegroundColor Gray
Write-Host "     python -m uvicorn app.main:app --reload" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. In another terminal, start the frontend:" -ForegroundColor White
Write-Host "     cd frontend" -ForegroundColor Gray
Write-Host "     python -m http.server 8080" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Open http://localhost:8080 in your browser" -ForegroundColor White
Write-Host ""
Write-Host "Or use Docker Compose:" -ForegroundColor Yellow
Write-Host "  docker-compose up -d" -ForegroundColor Gray
Write-Host ""
