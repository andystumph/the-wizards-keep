# Configuration Guide

Understanding every configuration file in The Wizard's Keep.

## Table of Contents

- [Environment Variables](#environment-variables)
- [Python Dependencies](#python-dependencies)
- [Python Configuration](#python-configuration)
- [Docker Configuration](#docker-configuration)
- [Kubernetes Configuration](#kubernetes-configuration)
- [Git Configuration](#git-configuration)

---

## Environment Variables

### `.env.example` File

**Location**: `backend/.env.example`

**What is it?**: Template file showing what environment variables your application needs.

**Why we have it**:
- 📋 **Documentation**: Shows developers what variables are required
- 🔒 **Security**: Keeps actual secrets out of git (you create `.env` from this)
- 👥 **Onboarding**: New developers know what to configure

**How to use it**:

```powershell
# 1. Copy the example file to create your .env file
cd backend
Copy-Item .env.example .env

# 2. Edit .env with your actual values
notepad .env

# 3. Never commit .env to git (it's in .gitignore)
```

**File contents explained**:

```dotenv
# Database Configuration
# =====================
# Connection string: postgresql://username:password@host:port/database_name
DATABASE_URL=postgresql://wizard:wizard123@localhost:5432/wizards_keep

# Individual components (used by Docker Compose)
POSTGRES_USER=wizard              # Database username
POSTGRES_PASSWORD=wizard123       # Database password (CHANGE IN PRODUCTION!)
POSTGRES_DB=wizards_keep         # Database name

# Application Configuration
# ========================
APP_NAME="The Wizard's Keep"     # Shows in API docs
APP_VERSION=1.0.0                 # Semantic versioning
DEBUG=true                        # true = detailed errors (dev only!)
LOG_LEVEL=INFO                    # DEBUG, INFO, WARNING, ERROR, CRITICAL

# API Configuration
# ================
API_HOST=0.0.0.0                  # 0.0.0.0 = listen on all network interfaces
API_PORT=8000                     # Port for backend API
CORS_ORIGINS=["http://localhost:8080", "http://localhost:3000"]  # Allowed frontend URLs

# Security Configuration
# =====================
# CRITICAL: Generate a secure random key for production!
# python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256                   # JWT signing algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=30    # How long users stay logged in

# Game Configuration
# =================
MAX_PLAYER_NAME_LENGTH=50         # Prevent extremely long names
STARTING_HEALTH=100               # New player health
STARTING_LOCATION_ID=1            # Where new players begin
```

**Common customizations**:

| Variable | Development | Production |
|----------|-------------|------------|
| `DEBUG` | `true` | `false` |
| `LOG_LEVEL` | `DEBUG` | `WARNING` |
| `POSTGRES_PASSWORD` | `wizard123` | Strong random password |
| `SECRET_KEY` | Any value | Cryptographically random |
| `DATABASE_URL` | `localhost` | Cloud database URL |

**Security best practices**:
1. ✅ Never commit `.env` files
2. ✅ Use different `.env` for dev/staging/prod
3. ✅ Generate strong `SECRET_KEY` for production
4. ✅ Rotate passwords regularly
5. ✅ Use environment variables in CI/CD, not `.env` files

---

## Python Dependencies

### Understanding Requirements Files

We have **two** requirements files for different purposes:

#### `requirements.txt` - Production Dependencies

**Location**: `backend/requirements.txt`

**What is it?**: Lists all packages needed to **run** the application in production.

**When to use it**:
- Deploying to production
- Building Docker images
- Running the application

**Contents explained**:

```pip-requirements
# Web Framework
# =============
fastapi==0.109.0              # Main web framework
uvicorn[standard]==0.27.0     # ASGI server to run FastAPI
python-multipart==0.0.6       # Parse form data and file uploads

# Database
# ========
sqlalchemy==2.0.25            # ORM for database operations
alembic==1.13.1               # Database migrations
psycopg2-binary==2.9.9        # PostgreSQL driver

# Data Validation
# ===============
pydantic==2.5.3               # Data validation using type hints
pydantic-settings==2.1.0      # Settings management with Pydantic

# Security
# ========
python-jose[cryptography]==3.3.0  # JWT token handling
passlib[bcrypt]==1.7.4            # Password hashing
python-dotenv==1.0.0              # Load .env files

# CORS
# ====
fastapi-cors==0.0.6           # Enable Cross-Origin Resource Sharing

# Testing (Minimal for production)
# =================================
pytest==7.4.4                 # Test framework
pytest-asyncio==0.23.3        # Test async functions
pytest-cov==4.1.0             # Code coverage
httpx==0.26.0                 # HTTP client for testing

# Code Quality
# ============
black==24.1.1                 # Code formatter
flake8==7.0.0                 # Style checker
mypy==1.8.0                   # Type checker
isort==5.13.2                 # Import sorter
pylint==3.0.3                 # Code analyzer

# Security Scanning
# =================
bandit==1.7.6                 # Security issue scanner
safety==3.0.1                 # Check for vulnerable dependencies

# Type Stubs
# ==========
types-passlib==1.7.7.20240106  # Type hints for passlib
sqlalchemy[mypy]==2.0.25       # Type hints for SQLAlchemy
```

**Version pinning explained**:
- `==0.109.0` - **Exact version** (most secure, reproducible)
- `>=0.109.0` - Any version 0.109.0 or higher (more flexible, risky)
- `~=0.109.0` - Compatible versions (0.109.x, not 0.110.0)

We use exact versions (`==`) for maximum reproducibility.

**Install production dependencies**:
```powershell
pip install -r requirements.txt
```

---

#### `requirements-dev.txt` - Development Dependencies

**Location**: `backend/requirements-dev.txt`

**What is it?**: Additional packages needed only for **development** (not production).

**When to use it**:
- Local development
- Running tests
- Code debugging

**Contents explained**:

```pip-requirements
# Development dependencies
# =======================
-r requirements.txt           # Include all production dependencies first

# Additional dev tools
# ====================
ipython==8.20.0               # Enhanced Python shell
  # Features:
  # - Syntax highlighting
  # - Tab completion
  # - ? for help
  # Usage: ipython

ipdb==0.13.13                 # IPython debugger
  # Features:
  # - Set breakpoints: import ipdb; ipdb.set_trace()
  # - Step through code
  # - Inspect variables
  # Usage: Add breakpoint in code

pre-commit==3.6.0             # Git hooks framework
  # Features:
  # - Run checks before committing
  # - Auto-format code
  # - Block bad commits
  # Usage: pre-commit install
```

**Why separate files?**

| Reason | Benefit |
|--------|---------|
| **Smaller production images** | Docker images are 50% smaller without dev tools |
| **Security** | Fewer packages = smaller attack surface |
| **Clarity** | Know what's essential vs. nice-to-have |
| **Speed** | Production installs are faster |

**Install development dependencies**:
```powershell
pip install -r requirements-dev.txt
```

**The `-r` directive**:
```pip-requirements
-r requirements.txt    # This line means "include requirements.txt"
```
So `requirements-dev.txt` includes **both** production and development packages.

---

### Updating Dependencies

**Check for updates**:
```powershell
pip list --outdated
```

**Update a package**:
```powershell
# 1. Update the package
pip install --upgrade fastapi

# 2. Update requirements.txt with new version
pip freeze | Select-String "fastapi" > temp.txt
# Manually copy version to requirements.txt
```

**Check for security vulnerabilities**:
```powershell
safety check
# or
pip-audit  # Alternative tool
```

---

## Python Configuration

### `pyproject.toml`

**Location**: `backend/pyproject.toml`

**What is it?**: Modern Python project configuration file (PEP 518).

**Purpose**: Configure Python tools (black, pytest, mypy) in one place.

**Contents explained**:

```toml
[tool.black]
# Black code formatter configuration
line-length = 88              # Max characters per line
target-version = ['py311']    # Python version to target
include = '\.pyi?$'           # Format .py and .pyi files
extend-exclude = '''          # Don't format these
/(
  migrations                  # Database migrations (generated)
  | venv                      # Virtual environment
  | \.git                     # Git directory
)/
'''

[tool.pytest.ini_options]
# pytest test runner configuration
testpaths = ["tests"]         # Where to find tests
python_files = ["test_*.py"]  # Test file pattern
python_classes = ["Test*"]    # Test class pattern
python_functions = ["test_*"] # Test function pattern
addopts = """
    --cov=app                 # Measure coverage for 'app' directory
    --cov-report=html         # Generate HTML coverage report
    --cov-report=term-missing # Show missing lines in terminal
    -v                        # Verbose output
"""

[tool.mypy]
# mypy type checker configuration
python_version = "3.11"       # Python version
plugins = ["pydantic.mypy"]   # Enable Pydantic plugin
ignore_missing_imports = true # Don't error on missing type stubs
disallow_untyped_defs = false # Allow functions without type hints
strict_optional = true        # None must be explicitly allowed

[tool.isort]
# isort import sorter configuration
profile = "black"             # Compatible with black
line_length = 88              # Match black's line length
multi_line_output = 3         # Vertical hanging indent
include_trailing_comma = true # Add trailing comma
force_grid_wrap = 0           # Don't force grid wrapping
use_parentheses = true        # Use parentheses for multi-line
ensure_newline_before_comments = true
```

**Why use pyproject.toml?**
- ✅ One file for all tools (vs. multiple config files)
- ✅ Modern Python standard
- ✅ Version controlled (everyone uses same settings)
- ✅ Tool-agnostic (supported by many tools)

---

### `setup.cfg`

**Location**: `backend/setup.cfg`

**What is it?**: Legacy configuration file (still used by some tools).

**Contents explained**:

```ini
[flake8]
# flake8 linter configuration
max-line-length = 88          # Match black's line length
extend-ignore = E203, W503    # Ignore conflicts with black
exclude =
    .git,                     # Git directory
    __pycache__,              # Python cache
    migrations,               # Database migrations
    venv,                     # Virtual environment
    .venv

[mypy]
# Additional mypy configuration
plugins = pydantic.mypy
ignore_missing_imports = True

[coverage:run]
# Coverage.py configuration
source = app                  # Measure coverage for 'app'
omit =
    */tests/*                 # Don't measure test coverage
    */migrations/*            # Don't measure migrations

[coverage:report]
# Coverage report settings
precision = 2                 # 2 decimal places (95.23%)
show_missing = True           # Show which lines not covered
skip_covered = False          # Show fully covered files
```

**Why both pyproject.toml and setup.cfg?**
- Some tools only support `setup.cfg` (like flake8)
- Gradual migration to `pyproject.toml`
- Eventually `pyproject.toml` will replace `setup.cfg`

---

## Docker Configuration

### `.dockerignore`

**Location**: `backend/.dockerignore`, `frontend/.dockerignore`

**What is it?**: Lists files to exclude from Docker images (like `.gitignore` for Docker).

**Why we need it**:
- 🚀 **Faster builds**: Don't copy unnecessary files
- 📦 **Smaller images**: Less bloat = smaller downloads
- 🔒 **Security**: Don't include secrets or test data

**Contents explained**:

```dockerignore
# Python
__pycache__/              # Python bytecode cache
*.py[cod]                 # Compiled Python files
*$py.class                # More compiled files
*.so                      # Shared objects
.Python                   # Python build artifacts

# Virtual environments
venv/                     # Virtual environment
.venv/                    # Alternative venv name
env/                      # Another venv name
ENV/                      # Yet another venv name

# Testing
.pytest_cache/            # pytest cache
.coverage                 # Coverage data
htmlcov/                  # Coverage HTML reports
*.cover                   # Coverage files
.hypothesis/              # Hypothesis testing cache

# Development
.env                      # Environment variables (secrets!)
.env.local                # Local overrides
.vscode/                  # VS Code settings
.idea/                    # PyCharm settings
*.swp                     # Vim swap files
*.swo                     # More vim files
*~                        # Backup files

# Documentation
*.md                      # Markdown files (not needed in image)
docs/                     # Documentation directory

# Git
.git/                     # Git repository
.gitignore                # Git ignore file
.gitattributes            # Git attributes

# CI/CD
.github/                  # GitHub Actions

# Docker
Dockerfile*               # Dockerfiles themselves
docker-compose*.yml       # Docker Compose files
.dockerignore             # This file
```

**Impact example**:
- ❌ **Without .dockerignore**: 500 MB image (includes venv, tests, git)
- ✅ **With .dockerignore**: 250 MB image (only necessary files)

---

### `Dockerfile.backend`

**Location**: `backend/Dockerfile.backend`

**What is it?**: Instructions to build the backend Docker image.

**Multi-stage build explained**:

```dockerfile
# ============================================
# Stage 1: Builder (temporary)
# ============================================
FROM python:3.11-slim as builder
# Why slim? Smaller base image (150MB vs 900MB)

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \                    # C compiler for psycopg2
    postgresql-client \      # PostgreSQL client libraries
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy only requirements first (Docker layer caching!)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# --no-cache-dir: Don't save pip cache (reduces image size)

# ============================================
# Stage 2: Runtime (final image)
# ============================================
FROM python:3.11-slim
# Start fresh with slim image (don't include build tools)

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
# Why? Don't run as root in containers (security best practice)

# Expose port
EXPOSE 8000

# Health check (Kubernetes/Docker Compose use this)
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

# Start application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Why multi-stage?**
- ✅ **Smaller**: Final image doesn't include build tools
- ✅ **Faster**: Layer caching speeds up rebuilds
- ✅ **Secure**: Fewer tools = fewer vulnerabilities

**Layer caching**:
```dockerfile
# ❌ Bad: Changes to code rebuild everything
COPY . .
RUN pip install -r requirements.txt

# ✅ Good: Changes to code don't rebuild dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

---

### `docker-compose.yml`

**Location**: `docker-compose.yml`

**What is it?**: Defines multiple services and how they work together.

**Full explanation**:

```yaml
version: '3.8'
# Docker Compose file format version

services:
  # ==========================
  # Service 1: Database
  # ==========================
  database:
    image: postgres:15-alpine
    # Why alpine? Lightweight (40MB vs 150MB)
    
    container_name: wizards-keep-db
    # Fixed name (easier to reference)
    
    environment:
      POSTGRES_USER: wizard
      POSTGRES_PASSWORD: wizard123
      POSTGRES_DB: wizards_keep
      # Environment variables configure PostgreSQL
    
    ports:
      - "5432:5432"
      # host:container port mapping
      # Access from host: localhost:5432
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
      # Named volume: data persists after container stops
    
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U wizard"]
      # Check if database is ready
      interval: 10s
      timeout: 5s
      retries: 5
      # Try every 10s, timeout after 5s, fail after 5 retries
    
    networks:
      - wizards-keep-network
      # Custom network for service communication

  # ==========================
  # Service 2: Backend API
  # ==========================
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
      # Build from local Dockerfile
    
    container_name: wizards-keep-backend
    
    environment:
      DATABASE_URL: postgresql://wizard:wizard123@database:5432/wizards_keep
      # Note: "database" hostname (Docker DNS resolves to database service)
      DEBUG: "true"
      LOG_LEVEL: INFO
    
    ports:
      - "8000:8000"
    
    depends_on:
      database:
        condition: service_healthy
        # Wait for database health check to pass
    
    volumes:
      - ./backend:/app
      # Mount local directory (changes reflect immediately)
      # Good for development, remove for production
    
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    # --reload: Auto-restart on code changes (dev only!)
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    
    networks:
      - wizards-keep-network

  # ==========================
  # Service 3: Frontend
  # ==========================
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile.frontend
    
    container_name: wizards-keep-frontend
    
    ports:
      - "8080:80"
      # Nginx serves on port 80 inside container
      # Access from host: localhost:8080
    
    depends_on:
      - backend
      # Start after backend
    
    networks:
      - wizards-keep-network

  # ==========================
  # Service 4: DB Initializer
  # ==========================
  db-init:
    build:
      context: ./backend
      dockerfile: Dockerfile.backend
    
    container_name: wizards-keep-db-init
    
    environment:
      DATABASE_URL: postgresql://wizard:wizard123@database:5432/wizards_keep
    
    depends_on:
      database:
        condition: service_healthy
    
    command: python scripts/init_db.py
    # Run once to populate database
    
    restart: "no"
    # Don't restart (only runs once)
    
    networks:
      - wizards-keep-network

# ==========================
# Volumes (persistent data)
# ==========================
volumes:
  postgres_data:
    # Named volume managed by Docker
    # Data persists between container restarts
    # Location: /var/lib/docker/volumes/wizards-keep_postgres_data

# ==========================
# Networks
# ==========================
networks:
  wizards-keep-network:
    driver: bridge
    # Bridge network: containers can communicate by name
    # database:5432, backend:8000, etc.
```

**Common commands**:

```powershell
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Stop and remove volumes (delete database data)
docker-compose down -v

# Rebuild images
docker-compose build

# Restart a single service
docker-compose restart backend
```

---

## Kubernetes Configuration

Kubernetes uses multiple YAML files. Here's what each does:

### `00-namespace.yaml` - Organize Resources

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: wizards-keep
# Namespaces isolate resources
# Like folders for your Kubernetes objects
```

### `01-configmap.yaml` - Non-Secret Configuration

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: app-config
data:
  APP_NAME: "The Wizard's Keep"
  LOG_LEVEL: "INFO"
# ConfigMaps store configuration that isn't secret
# Mounted as environment variables or files
```

### `02-secrets.yaml` - Sensitive Data

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: app-secrets
type: Opaque
stringData:
  POSTGRES_PASSWORD: "wizard123"
  SECRET_KEY: "your-secret-key"
# Secrets store passwords, keys, etc.
# Encoded (not encrypted by default - use external secrets in production)
```

### `03-pvc.yaml` - Persistent Storage

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: postgres-pvc
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 5Gi
# PVC requests storage from cluster
# Data survives pod deletion
```

### `04-database-deployment.yaml` - Database Pods

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: database
spec:
  replicas: 1                # Number of pods
  template:
    spec:
      containers:
      - name: postgres
        image: postgres:15-alpine
        env:
          - name: POSTGRES_PASSWORD
            valueFrom:
              secretKeyRef:    # Load from Secret
                name: app-secrets
                key: POSTGRES_PASSWORD
        volumeMounts:
          - name: postgres-storage
            mountPath: /var/lib/postgresql/data
      volumes:
        - name: postgres-storage
          persistentVolumeClaim:
            claimName: postgres-pvc
# Deployment manages replica pods
# Ensures desired number of pods are running
```

### `05-database-service.yaml` - Database Network Access

```yaml
apiVersion: v1
kind: Service
metadata:
  name: database
spec:
  type: ClusterIP           # Internal only (not exposed outside cluster)
  ports:
    - port: 5432
      targetPort: 5432
  selector:
    app: database           # Routes to pods with this label
# Service provides stable DNS name: database.wizards-keep.svc.cluster.local
# Simplified: just "database" within same namespace
```

### Other K8s files follow same patterns for backend, frontend, etc.

---

## Git Configuration

### `.gitignore`

**Location**: `.gitignore`

**What is it?**: Files to exclude from git version control.

**Categories explained**:

```gitignore
# ===========================
# Python
# ===========================
__pycache__/              # Compiled bytecode (regenerated automatically)
*.py[cod]                 # More compiled files
venv/                     # Virtual environment (too large, user-specific)
.env                      # SECRETS! Never commit!

# ===========================
# Testing
# ===========================
.pytest_cache/            # Test cache (regenerated)
.coverage                 # Coverage data (regenerated)
htmlcov/                  # HTML reports (regenerated)

# ===========================
# IDE
# ===========================
.vscode/                  # VS Code settings (user preference)
.idea/                    # PyCharm settings (user preference)
*.swp                     # Vim temporary files

# ===========================
# OS
# ===========================
.DS_Store                 # macOS folder metadata
Thumbs.db                 # Windows thumbnail cache
desktop.ini               # Windows folder settings

# ===========================
# Logs
# ===========================
*.log                     # Log files (too large, generated at runtime)
logs/                     # Log directory

# ===========================
# Database
# ===========================
*.db                      # SQLite databases (local dev only)
*.sqlite                  # SQLite databases

# ===========================
# Docker
# ===========================
# Note: We DO commit Dockerfiles
# We DON'T commit built images (too large)
```

**Why ignore these?**
- ✅ **Security**: `.env` contains secrets
- ✅ **Size**: Virtual environments and logs are huge
- ✅ **User-specific**: IDE settings differ per developer
- ✅ **Generated**: Can be recreated (cache, compiled files)

---

### `.gitattributes`

**Location**: `.gitattributes`

**What is it?**: Controls how git handles files (line endings, diffs, etc.).

**Contents explained**:

```gitattributes
# Auto-detect text files and normalize line endings to LF
* text=auto

# Source code: Always use LF (Unix style)
*.py text eol=lf
*.js text eol=lf
*.html text eol=lf
*.css text eol=lf
*.md text eol=lf
*.yml text eol=lf
*.yaml text eol=lf
*.json text eol=lf
*.sh text eol=lf

# Windows scripts: Always use CRLF
*.ps1 text eol=crlf
*.bat text eol=crlf
*.cmd text eol=crlf

# Binary files: Don't try to diff or merge
*.png binary
*.jpg binary
*.jpeg binary
*.gif binary
*.ico binary
*.db binary
*.sqlite binary
```

**Line ending explained**:
- **LF** (`\n`): Unix/Linux/Mac line ending
- **CRLF** (`\r\n`): Windows line ending
- **Why this matters**: Shell scripts won't work with CRLF endings

**What `text=auto` does**:
1. On checkout: Converts to your OS's line ending
2. On commit: Normalizes to LF in git
3. Result: Everyone can work on any OS

---

## Summary Checklist

When starting development:

- [ ] Copy `.env.example` to `.env` and customize
- [ ] Install dependencies: `pip install -r requirements-dev.txt`
- [ ] Understand what each tool does (see TOOLS_AND_FRAMEWORKS.md)
- [ ] Read `pyproject.toml` to see tool configurations
- [ ] Check `.dockerignore` to understand what's excluded
- [ ] Review `docker-compose.yml` to understand service setup
- [ ] Look at `requirements.txt` to see production dependencies

For production deployment:

- [ ] Generate secure `SECRET_KEY`
- [ ] Use strong `POSTGRES_PASSWORD`
- [ ] Set `DEBUG=false`
- [ ] Set `LOG_LEVEL=WARNING` or `ERROR`
- [ ] Use environment variables in Kubernetes, not `.env` files
- [ ] Review security settings in all config files

---

## Need Help?

- **Environment issues**: Check `.env` file matches `.env.example`
- **Dependency issues**: Try `pip install --upgrade -r requirements-dev.txt`
- **Docker issues**: Check `.dockerignore` isn't excluding needed files
- **Git issues**: Check `.gitignore` and `.gitattributes`

Happy configuring! 🔧
