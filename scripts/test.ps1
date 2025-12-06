# Test Runner Script for Windows (PowerShell)
#
# Runs all tests, linting, and security checks

$ErrorActionPreference = "Stop"

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  The Wizard's Keep - Test Suite" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    & .\venv\Scripts\Activate.ps1
}
else {
    Write-Host "❌ Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    exit 1
}

Set-Location backend

$failed = $false

# Run unit tests
Write-Host "Running unit tests..." -ForegroundColor Yellow
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Unit tests failed" -ForegroundColor Red
    $failed = $true
}
else {
    Write-Host "✅ Unit tests passed" -ForegroundColor Green
}
Write-Host ""

# Run Black (formatter check)
Write-Host "Checking code formatting with Black..." -ForegroundColor Yellow
black --check app/ tests/
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Code formatting issues found. Run: black app/ tests/" -ForegroundColor Red
    $failed = $true
}
else {
    Write-Host "✅ Code formatting is correct" -ForegroundColor Green
}
Write-Host ""

# Run flake8 (linter)
Write-Host "Running flake8 linter..." -ForegroundColor Yellow
flake8 app/ tests/ --max-line-length=100 --extend-ignore=E203,W503
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Linting issues found" -ForegroundColor Red
    $failed = $true
}
else {
    Write-Host "✅ No linting issues" -ForegroundColor Green
}
Write-Host ""

# Run mypy (type checker)
Write-Host "Running mypy type checker..." -ForegroundColor Yellow
mypy app/ --ignore-missing-imports
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Type checking issues found" -ForegroundColor Red
    $failed = $true
}
else {
    Write-Host "✅ Type checking passed" -ForegroundColor Green
}
Write-Host ""

# Run bandit (security scanner)
Write-Host "Running bandit security scanner..." -ForegroundColor Yellow
bandit -r app/ -ll
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Security issues found" -ForegroundColor Red
    $failed = $true
}
else {
    Write-Host "✅ No security issues" -ForegroundColor Green
}
Write-Host ""

Set-Location ..

# Summary
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
if ($failed) {
    Write-Host "  Test Suite: FAILED ❌" -ForegroundColor Red
    exit 1
}
else {
    Write-Host "  Test Suite: PASSED ✅" -ForegroundColor Green
    Write-Host ""
    Write-Host "  Coverage report: backend/htmlcov/index.html" -ForegroundColor Yellow
    exit 0
}
