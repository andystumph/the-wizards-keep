#!/bin/bash
# Setup Script for Linux/Mac
#
# This script sets up the development environment for The Wizard's Keep

set -e  # Exit on error

echo "═══════════════════════════════════════════════════"
echo "  The Wizard's Keep - Development Setup"
echo "═══════════════════════════════════════════════════"
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
echo "Checking prerequisites..."

# Check Python
if ! command_exists python3; then
    echo "❌ Python is not installed. Please install Python 3.11 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found: $PYTHON_VERSION"

# Check Docker
if ! command_exists docker; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi

DOCKER_VERSION=$(docker --version)
echo "✅ Found: $DOCKER_VERSION"

# Check Git
if ! command_exists git; then
    echo "⚠️  Git is not installed. Git is recommended but optional."
else
    GIT_VERSION=$(git --version)
    echo "✅ Found: $GIT_VERSION"
fi

echo ""
echo "Setting up Python virtual environment..."

# Create virtual environment
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
python -m pip install --upgrade pip

# Install backend dependencies
echo ""
echo "Installing backend dependencies..."
cd backend
pip install -r requirements-dev.txt
cd ..
echo "✅ Backend dependencies installed"

# Create .env file if it doesn't exist
echo ""
echo "Setting up environment configuration..."
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    echo "✅ Created .env file from .env.example"
    echo "⚠️  Please review and update backend/.env with your settings"
else
    echo ".env file already exists. Skipping."
fi

# Start database with Docker
echo ""
echo "Starting PostgreSQL database..."
docker run -d \
    --name wizards-keep-db \
    -p 5432:5432 \
    -e POSTGRES_USER=wizard \
    -e POSTGRES_PASSWORD=wizard123 \
    -e POSTGRES_DB=wizards_keep \
    postgres:15-alpine 2>/dev/null || docker start wizards-keep-db

echo "✅ Database container started"

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 3

# Initialize database
echo ""
echo "Initializing game database..."
cd backend
python scripts/init_db.py
cd ..
echo "✅ Database initialized with game content"

echo ""
echo "═══════════════════════════════════════════════════"
echo "  Setup Complete! 🎉"
echo "═══════════════════════════════════════════════════"
echo ""
echo "To start the application:"
echo ""
echo "  1. Start the backend:"
echo "     cd backend"
echo "     python -m uvicorn app.main:app --reload"
echo ""
echo "  2. In another terminal, start the frontend:"
echo "     cd frontend"
echo "     python -m http.server 8080"
echo ""
echo "  3. Open http://localhost:8080 in your browser"
echo ""
echo "Or use Docker Compose:"
echo "  docker-compose up -d"
echo ""
