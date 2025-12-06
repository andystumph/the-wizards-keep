# Tools and Frameworks Guide

A comprehensive guide to every tool, framework, and technology used in The Wizard's Keep.

## Table of Contents

- [Backend Framework](#backend-framework)
- [Database](#database)
- [Frontend](#frontend)
- [Testing](#testing)
- [Code Quality](#code-quality)
- [Containerization](#containerization)
- [Orchestration](#orchestration)
- [CI/CD](#cicd)
- [Development Tools](#development-tools)

---

## Backend Framework

### FastAPI

**What is it?**: FastAPI is a modern, high-performance web framework for building APIs with Python 3.7+ based on standard Python type hints.

**Why we use it**:
- ⚡ **Fast**: One of the fastest Python frameworks (comparable to NodeJS and Go)
- 🔒 **Type Safe**: Uses Python type hints for automatic validation
- 📚 **Auto Documentation**: Generates interactive API docs automatically
- 🐍 **Modern Python**: Supports async/await for concurrent requests
- ✅ **Standards-Based**: Built on OpenAPI and JSON Schema

**Example from our project**:
```python
from fastapi import FastAPI

app = FastAPI(title="The Wizard's Keep API")

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
```

**Learn more**: https://fastapi.tiangolo.com/

---

### Uvicorn

**What is it?**: Uvicorn is an ASGI (Asynchronous Server Gateway Interface) web server for Python.

**Why we use it**:
- Runs FastAPI applications
- Supports async operations
- Hot-reloading in development mode
- Production-ready performance

**How we use it**:
```powershell
# Development (with auto-reload)
uvicorn app.main:app --reload

# Production
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

**Learn more**: https://www.uvicorn.org/

---

### Pydantic

**What is it?**: Pydantic is a data validation library that uses Python type hints.

**Why we use it**:
- 🔍 **Automatic Validation**: Validates incoming data against schemas
- 🛡️ **Type Safety**: Catches errors before they reach your code
- 📝 **Clear Errors**: Provides detailed validation error messages
- 🔄 **Serialization**: Converts between Python objects and JSON

**Example from our project**:
```python
from pydantic import BaseModel

class PlayerCreate(BaseModel):
    username: str  # Required string
    character_name: str  # Required string
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "thornwind",
                "character_name": "Kael Thornwind"
            }
        }
```

If someone tries to create a player without a username, Pydantic automatically returns a 422 error with details.

**Learn more**: https://docs.pydantic.dev/

---

## Database

### PostgreSQL

**What is it?**: PostgreSQL is a powerful, open-source relational database system.

**Why we use it**:
- 🏆 **Most Advanced**: Supports complex queries, transactions, and JSON
- 🔒 **ACID Compliant**: Guarantees data integrity
- 🔗 **Relationships**: Perfect for our linked locations, items, and players
- 📊 **Performance**: Handles millions of records efficiently
- 🆓 **Open Source**: Free and community-supported

**Key concepts**:
- **Tables**: Store data in rows and columns (like spreadsheets)
- **Foreign Keys**: Link tables together (e.g., player → game_state)
- **Indexes**: Speed up queries on commonly searched columns
- **Transactions**: Ensure operations complete fully or not at all

**Example from our project**:
```sql
-- Players table
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    character_name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Game state links to player
CREATE TABLE game_states (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    health INTEGER DEFAULT 100
);
```

**Learn more**: https://www.postgresql.org/docs/

---

### SQLAlchemy ORM

**What is it?**: SQLAlchemy is an Object-Relational Mapper (ORM) that lets you work with database tables as Python classes.

**Why we use it**:
- 🐍 **Pythonic**: Write Python instead of SQL
- 🔒 **SQL Injection Safe**: Automatically escapes dangerous input
- 🔄 **Database Agnostic**: Switch databases (PostgreSQL → MySQL) with minimal changes
- 🏗️ **Relationships**: Automatically handles foreign keys and joins
- ⚡ **Efficient**: Lazy loading and eager loading options

**ORM Concept**:
```
Database Table          Python Class
--------------          ------------
players                 class Player
  ├─ id                   ├─ id: int
  ├─ username             ├─ username: str
  └─ character_name       └─ character_name: str
```

**Example from our project**:
```python
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    character_name = Column(String(100), nullable=False)
```

**Without ORM** (raw SQL):
```python
cursor.execute(
    "INSERT INTO players (username, character_name) VALUES (%s, %s)",
    ("thornwind", "Kael Thornwind")
)
```

**With ORM** (SQLAlchemy):
```python
player = Player(username="thornwind", character_name="Kael Thornwind")
db.add(player)
db.commit()
```

**Learn more**: https://docs.sqlalchemy.org/

---

### Alembic

**What is it?**: Alembic is a database migration tool for SQLAlchemy.

**Why we use it**:
- 📝 **Version Control for Database**: Track schema changes like git tracks code
- ⬆️ **Migrations**: Update database schema without losing data
- ⬇️ **Rollbacks**: Undo schema changes if something goes wrong
- 👥 **Team Collaboration**: Everyone gets the same database structure

**Example workflow**:
```powershell
# 1. Make changes to models.py
# (e.g., add new column to Player)

# 2. Generate migration
alembic revision --autogenerate -m "Add email to players"

# 3. Review the generated migration
# alembic/versions/abc123_add_email_to_players.py

# 4. Apply migration
alembic upgrade head

# 5. If needed, rollback
alembic downgrade -1
```

**Learn more**: https://alembic.sqlalchemy.org/

---

### psycopg2

**What is it?**: psycopg2 is a PostgreSQL adapter for Python.

**Why we use it**:
- 🔌 **Database Driver**: Connects Python to PostgreSQL
- ⚡ **Performance**: Written in C for speed
- 🔒 **Secure**: Handles connection pooling and escaping

**Note**: SQLAlchemy uses psycopg2 under the hood. You typically don't use it directly.

**Learn more**: https://www.psycopg.org/

---

## Frontend

### HTML5

**What is it?**: HyperText Markup Language - the standard for web pages.

**Why we use it**:
- 📄 **Structure**: Defines page content and layout
- 🌐 **Universal**: Works in every browser
- 🎨 **Semantic**: Tags like `<section>`, `<article>` add meaning

**Example from our project**:
```html
<div class="game-screen" id="gameScreen">
    <div class="status-bar">
        <span>HP: <span id="health">100</span>/<span id="maxHealth">100</span></span>
        <span>Level: <span id="level">1</span></span>
    </div>
    <div class="output" id="output"></div>
    <input type="text" id="commandInput" placeholder="Enter command...">
</div>
```

---

### CSS3

**What is it?**: Cascading Style Sheets - controls visual styling.

**Why we use it**:
- 🎨 **Styling**: Colors, fonts, spacing, animations
- 📱 **Responsive**: Adapts to different screen sizes
- 🎭 **Themes**: Easy to change appearance

**Example from our project** (retro terminal style):
```css
:root {
    --c64-blue: #352879;
    --c64-light-blue: #7c70da;
    --terminal-green: #33ff33;
}

body {
    background-color: var(--c64-blue);
    color: var(--terminal-green);
    font-family: 'Courier New', monospace;
}
```

---

### JavaScript (ES6+)

**What is it?**: Programming language that runs in web browsers.

**Why we use it**:
- 🎮 **Interactivity**: Handle user input, update UI dynamically
- 🌐 **API Calls**: Communicate with backend via fetch()
- 💾 **State Management**: Track game state on client side

**Example from our project**:
```javascript
async function executeCommand(command) {
    const response = await fetch(`${API_BASE_URL}/game/command`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            player_id: currentPlayer.id,
            command: command
        })
    });
    
    const result = await response.json();
    displayMessage(result.message);
    updateGameState(result.game_state);
}
```

---

## Testing

### pytest

**What is it?**: A Python testing framework.

**Why we use it**:
- ✅ **Simple Syntax**: Write tests as simple functions
- 🔧 **Fixtures**: Reusable test setup (e.g., database session)
- 📊 **Coverage**: Measure what code is tested
- 🎯 **Assertions**: Clear, readable test assertions

**Example from our project**:
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_player():
    response = client.post(
        "/api/v1/players/",
        json={"username": "testuser", "character_name": "Test Hero"}
    )
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

**Learn more**: https://docs.pytest.org/

---

### pytest-asyncio

**What is it?**: Plugin for testing async functions.

**Why we use it**:
- FastAPI uses async functions
- Allows testing async database operations

**Example**:
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

---

### pytest-cov

**What is it?**: Code coverage plugin for pytest.

**Why we use it**:
- 📊 **Measures Coverage**: Shows what % of code is tested
- 🎯 **Identifies Gaps**: Highlights untested code
- 📈 **Track Progress**: Watch coverage improve over time

**Usage**:
```powershell
pytest --cov=app --cov-report=html
# Opens htmlcov/index.html to see detailed coverage report
```

**Coverage goals**:
- 🟢 80%+ coverage: Good
- 🟡 60-80% coverage: Acceptable
- 🔴 <60% coverage: Needs improvement

---

### httpx

**What is it?**: HTTP client for Python with async support.

**Why we use it**:
- 🧪 **Testing**: TestClient uses httpx to simulate API requests
- ⚡ **Async**: Supports async/await
- 🔗 **HTTP/2**: Modern HTTP protocol support

**Example**:
```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/api/v1/players/")
assert response.status_code == 200
```

---

## Code Quality

### Black

**What is it?**: The "uncompromising" Python code formatter.

**Why we use it**:
- 🎨 **Consistent Style**: Everyone's code looks the same
- ⏱️ **Saves Time**: No debates about formatting
- 🤖 **Automatic**: Format on save or in CI/CD

**Example**:
```powershell
# Format all Python files
black backend/app

# Check without modifying
black --check backend/app
```

**Before Black**:
```python
def my_function(x,y,z):
    return x+y+z
```

**After Black**:
```python
def my_function(x, y, z):
    return x + y + z
```

**Learn more**: https://black.readthedocs.io/

---

### flake8

**What is it?**: Python linter that checks for style and programming errors.

**Why we use it**:
- 🐛 **Find Bugs**: Catches unused imports, undefined variables
- 📏 **Style Guide**: Enforces PEP 8 (Python's style guide)
- ⚠️ **Warnings**: Alerts to potential issues

**Example checks**:
- Unused imports
- Lines too long (>88 characters)
- Undefined variables
- Missing whitespace

**Usage**:
```powershell
flake8 backend/app
```

**Learn more**: https://flake8.pycqa.org/

---

### mypy

**What is it?**: Static type checker for Python.

**Why we use it**:
- 🔍 **Type Checking**: Catches type errors before runtime
- 📝 **Type Hints**: Enforces type annotations
- 🐛 **Early Detection**: Find bugs during development

**Example**:
```python
def add_numbers(a: int, b: int) -> int:
    return a + b

# mypy catches this error:
result = add_numbers("5", "10")  # Error: Expected int, got str
```

**Usage**:
```powershell
mypy backend/app
```

**Learn more**: https://mypy-lang.org/

---

### isort

**What is it?**: Automatically sorts Python imports.

**Why we use it**:
- 📚 **Organized Imports**: Groups stdlib, third-party, local imports
- 🤖 **Automatic**: Sort on save or in CI/CD
- 👥 **Consistent**: Everyone's imports match

**Example**:

**Before isort**:
```python
from app.models import Player
import os
from typing import List
from fastapi import FastAPI
```

**After isort**:
```python
import os
from typing import List

from fastapi import FastAPI

from app.models import Player
```

**Usage**:
```powershell
isort backend/app
```

**Learn more**: https://pycqa.github.io/isort/

---

### pylint

**What is it?**: Comprehensive Python linter.

**Why we use it**:
- 🔍 **Deep Analysis**: More thorough than flake8
- 📊 **Code Rating**: Scores your code out of 10
- 💡 **Suggestions**: Recommends improvements

**Usage**:
```powershell
pylint backend/app
```

**Learn more**: https://pylint.org/

---

### Bandit

**What is it?**: Security linter for Python.

**Why we use it**:
- 🔒 **Security Scanning**: Finds security vulnerabilities
- ⚠️ **Warnings**: Alerts to risky code patterns
- 🛡️ **Best Practices**: Enforces security standards

**Example findings**:
- Hardcoded passwords
- SQL injection vulnerabilities
- Use of `eval()` or `exec()`
- Insecure random number generation

**Usage**:
```powershell
bandit -r backend/app
```

**Learn more**: https://bandit.readthedocs.io/

---

## Containerization

### Docker

**What is it?**: Platform for building, running, and shipping applications in containers.

**Why we use it**:
- 📦 **Packaging**: Bundle app + dependencies in one container
- 🔄 **Consistency**: "Works on my machine" → "Works everywhere"
- ⚡ **Fast Startup**: Containers start in seconds
- 🏗️ **Isolation**: Each container is independent

**Key concepts**:

**Image**: Blueprint for a container (like a class)
**Container**: Running instance of an image (like an object)
**Dockerfile**: Recipe to build an image

**Example from our project** (`Dockerfile.backend`):
```dockerfile
# Start with Python 3.11
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Learn more**: https://docs.docker.com/

---

### Docker Compose

**What is it?**: Tool for running multi-container applications.

**Why we use it**:
- 🎼 **Orchestration**: Run multiple services together
- 🔗 **Networking**: Containers can communicate
- 📋 **Configuration**: Define everything in one YAML file
- ⚡ **One Command**: `docker-compose up` starts everything

**Example from our project**:
```yaml
services:
  database:
    image: postgres:15-alpine
    ports:
      - "5432:5432"
  
  backend:
    build: ./backend
    depends_on:
      - database
    ports:
      - "8000:8000"
  
  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "8080:80"
```

**Learn more**: https://docs.docker.com/compose/

---

### Nginx

**What is it?**: Web server and reverse proxy.

**Why we use it**:
- 🌐 **Static Files**: Serves HTML, CSS, JS efficiently
- ⚡ **Performance**: Handles thousands of concurrent connections
- 🔀 **Proxy**: Can forward requests to backend
- 🐳 **Production-Ready**: Industry standard

**Usage in our project**:
- Serves frontend files in production
- Lightweight (nginx:alpine image)

**Learn more**: https://nginx.org/en/docs/

---

## Orchestration

### Kubernetes (K8s)

**What is it?**: Container orchestration platform.

**Why we use it**:
- 🔄 **Auto-Scaling**: Add/remove containers based on load
- 🏥 **Self-Healing**: Restarts failed containers
- 📦 **Declarative**: Describe desired state, K8s makes it happen
- 🌐 **Production-Grade**: Used by Google, Netflix, Spotify

**Key concepts**:

**Pod**: Smallest unit, contains 1+ containers
**Deployment**: Manages replicas of pods
**Service**: Network endpoint to access pods
**ConfigMap**: Configuration data
**Secret**: Sensitive data (passwords, keys)
**PersistentVolume**: Storage that survives pod restarts

**Example from our project**:
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3  # Run 3 copies of backend
  template:
    spec:
      containers:
      - name: backend
        image: wizards-keep-backend:latest
        ports:
        - containerPort: 8000
```

**Learn more**: https://kubernetes.io/docs/

---

### Rancher Desktop

**What is it?**: Desktop application for running Kubernetes locally.

**Why we use it**:
- 🖥️ **Local K8s**: Run Kubernetes on Windows/Mac/Linux
- 🐳 **Docker Compatible**: Works with docker commands
- 🆓 **Free**: Open-source alternative to Docker Desktop
- 🎓 **Learning**: Perfect for education

**Learn more**: https://rancherdesktop.io/

---

## CI/CD

### GitHub Actions

**What is it?**: Automation platform built into GitHub.

**Why we use it**:
- 🤖 **Automation**: Run tests on every push/PR
- ✅ **Quality Gates**: Block merges if tests fail
- 🚀 **Deployment**: Auto-deploy to production
- 🆓 **Free**: 2000 minutes/month for public repos

**Example workflow** (`.github/workflows/ci-cd.yml`):
```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: pytest
      
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker image
        run: docker build -t app .
```

**Learn more**: https://docs.github.com/actions

---

## Development Tools

### python-dotenv

**What is it?**: Loads environment variables from `.env` files.

**Why we use it**:
- 🔐 **Secrets Management**: Keep passwords out of code
- ⚙️ **Configuration**: Different settings per environment
- 🔒 **Security**: `.env` files stay out of git

**Usage**:
```python
from dotenv import load_dotenv
import os

load_dotenv()  # Loads .env file
db_password = os.getenv("POSTGRES_PASSWORD")
```

**Learn more**: https://github.com/theskumar/python-dotenv

---

### IPython

**What is it?**: Enhanced Python interactive shell.

**Why we use it**:
- 🎨 **Syntax Highlighting**: Colorful, readable output
- 📝 **Tab Completion**: Auto-complete functions/variables
- 🔍 **Introspection**: Explore objects with `?` and `??`
- 🐛 **Debugging**: Better error messages

**Usage**:
```powershell
ipython
>>> from app.models import Player
>>> Player?  # Shows documentation
```

**Learn more**: https://ipython.org/

---

### pre-commit

**What is it?**: Framework for managing git hooks.

**Why we use it**:
- ✅ **Auto-Checks**: Run linters before committing
- 🚫 **Block Bad Code**: Prevent committing broken code
- 🎯 **Consistent**: All developers use same checks

**Example** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/psf/black
    hooks:
      - id: black
  - repo: https://github.com/pycqa/flake8
    hooks:
      - id: flake8
```

**Learn more**: https://pre-commit.com/

---

## Summary Table

| Category | Tool | Purpose | When You Use It |
|----------|------|---------|----------------|
| **Backend** | FastAPI | Web framework | Building REST APIs |
| | Uvicorn | ASGI server | Running FastAPI apps |
| | Pydantic | Validation | Defining data schemas |
| **Database** | PostgreSQL | Database | Storing game data |
| | SQLAlchemy | ORM | Python ↔ Database |
| | Alembic | Migrations | Updating database schema |
| **Frontend** | HTML5 | Structure | Building web pages |
| | CSS3 | Styling | Making pages beautiful |
| | JavaScript | Behavior | Adding interactivity |
| **Testing** | pytest | Test runner | Running tests |
| | pytest-cov | Coverage | Measuring test coverage |
| | httpx | HTTP client | Testing API endpoints |
| **Quality** | black | Formatter | Consistent code style |
| | flake8 | Linter | Finding style issues |
| | mypy | Type checker | Catching type errors |
| | bandit | Security | Finding vulnerabilities |
| **Containers** | Docker | Containerization | Packaging applications |
| | Docker Compose | Multi-container | Running all services |
| | Nginx | Web server | Serving frontend |
| **Orchestration** | Kubernetes | Container orchestration | Production deployment |
| | Rancher Desktop | Local K8s | Development/learning |
| **CI/CD** | GitHub Actions | Automation | Running tests/builds |
| **Dev Tools** | python-dotenv | Environment vars | Managing config |
| | IPython | Enhanced shell | Interactive debugging |
| | pre-commit | Git hooks | Pre-commit checks |

---

## Next Steps

1. **Read each tool's documentation** linked above
2. **Try modifying the code** to see how each tool works
3. **Run the commands** in this guide to understand the workflow
4. **Experiment**: Break things and fix them to learn!

Remember: You don't need to master everything at once. Start with the basics (FastAPI, SQLAlchemy, pytest) and gradually explore the others.
