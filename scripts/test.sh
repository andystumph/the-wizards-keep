#!/bin/bash
# Test Runner Script for Linux/Mac

set -e

echo "═══════════════════════════════════════════════════"
echo "  The Wizard's Keep - Test Suite"
echo "═══════════════════════════════════════════════════"
echo ""

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run setup.sh first."
    exit 1
fi

cd backend

failed=0

# Run unit tests
echo "Running unit tests..."
pytest tests/ -v --cov=app --cov-report=term-missing --cov-report=html || failed=1
if [ $failed -eq 0 ]; then
    echo "✅ Unit tests passed"
else
    echo "❌ Unit tests failed"
fi
echo ""

# Run Black (formatter check)
echo "Checking code formatting with Black..."
black --check app/ tests/ || {
    echo "❌ Code formatting issues found. Run: black app/ tests/"
    failed=1
}
echo "✅ Code formatting is correct"
echo ""

# Run isort (import sorting check)
echo "Checking import sorting with isort..."
isort --check-only app/ tests/ || {
    echo "❌ Import sorting issues found. Run: isort app/ tests/"
    failed=1
}
echo "✅ Import sorting is correct"
echo ""

# Run flake8 (linter)
echo "Running flake8 linter..."
flake8 app/ tests/ --max-line-length=100 --extend-ignore=E203,W503 || {
    echo "❌ Linting issues found"
    failed=1
}
echo "✅ No linting issues"
echo ""

# Run mypy (type checker)
echo "Running mypy type checker..."
mypy app/ --ignore-missing-imports || {
    echo "❌ Type checking issues found"
    failed=1
}
echo "✅ Type checking passed"
echo ""

# Run bandit (security scanner)
echo "Running bandit security scanner..."
bandit -r app/ -ll || {
    echo "❌ Security issues found"
    failed=1
}
echo "✅ No security issues"
echo ""

cd ..

# Summary
echo "═══════════════════════════════════════════════════"
if [ $failed -eq 1 ]; then
    echo "  Test Suite: FAILED ❌"
    exit 1
else
    echo "  Test Suite: PASSED ✅"
    echo ""
    echo "  Coverage report: backend/htmlcov/index.html"
    exit 0
fi
