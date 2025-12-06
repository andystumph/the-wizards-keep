# Getting Started - Complete Beginner's Guide

**Welcome!** This guide is for complete beginners who want to learn modern software development through a fun, practical project.

## 🤔 What Will I Learn?

By working through this project, you'll learn:

1. **Backend Development** - Building a server and API with Python
2. **Database Design** - Storing and retrieving data with PostgreSQL
3. **Frontend Development** - Creating user interfaces with HTML/CSS/JavaScript
4. **Containerization** - Packaging applications with Docker
5. **Testing** - Writing tests to ensure code quality
6. **CI/CD** - Automating testing and deployment
7. **Code Quality** - Using tools to maintain clean, secure code

**Don't worry if these terms are new to you!** We'll explain everything step by step.

---

## 📋 Prerequisites

### What You Need Installed

1. **Python 3.11+** - Programming language for the backend
   - Download: https://www.python.org/downloads/
   - Check version: `python --version`

2. **Docker Desktop or Rancher Desktop** - For running containers
   - Docker Desktop: https://www.docker.com/products/docker-desktop/
   - Rancher Desktop (free alternative): https://rancherdesktop.io/
   - Check: `docker --version`

3. **Git** (optional but recommended) - Version control
   - Download: https://git-scm.com/downloads
   - Check: `git --version`

4. **A Code Editor** - To view and edit code
   - Visual Studio Code (recommended): https://code.visualstudio.com/
   - Or any text editor you prefer

### Knowledge Prerequisites

**None!** This project is designed for learning. However, basic familiarity with:
- Using a command line/terminal (we'll show you the commands)
- Basic programming concepts (variables, functions)
- How web browsers work

...will help you get more out of it.

---

## 🗺️ Understanding the Project Structure

Before diving in, let's understand what you're looking at:

```
the-wizards-keep/
│
├── backend/           ← Python server (the "brains")
│   ├── app/          ← Application code
│   ├── tests/        ← Tests for the backend
│   └── scripts/      ← Helper scripts
│
├── frontend/          ← Web interface (what users see)
│   ├── index.html    ← Main web page
│   ├── css/          ← Styling (colors, fonts)
│   └── js/           ← Interactivity (JavaScript)
│
├── k8s/               ← Kubernetes configs (advanced deployment)
│
├── scripts/           ← Automation scripts
│   ├── setup.ps1     ← Windows setup script
│   └── test.ps1      ← Windows test script
│
├── docs/              ← Documentation (you are here!)
│
├── docker-compose.yml ← Runs all services together
│
└── README.md          ← Project overview
```

---

## 🚀 Step-by-Step Setup

### Step 1: Get the Code

**Option A: With Git (recommended)**
```powershell
git clone https://github.com/yourusername/the-wizards-keep.git
cd the-wizards-keep
```

**Option B: Download ZIP**
1. Go to GitHub repository
2. Click "Code" → "Download ZIP"
3. Extract to `C:\Code\the-wizards-keep`
4. Open PowerShell in that folder

---

### Step 2: Run the Application

**The easiest way - Docker Compose:**

```powershell
# Start all services (database, backend, frontend)
docker-compose up -d

# Wait 30 seconds for services to start

# Initialize the game world
docker-compose exec backend python scripts/init_db.py
```

**What just happened?**
1. ✅ PostgreSQL database started (stores game data)
2. ✅ Backend API started (handles game logic)
3. ✅ Frontend web server started (serves the UI)
4. ✅ Game world populated (locations, items, enemies)

---

### Step 3: Play the Game!

1. Open your web browser
2. Go to http://localhost:8080
3. Create a character
4. Start playing!

**Try these commands:**
- `LOOK` - See your surroundings
- `GO NORTH` - Move to another location
- `TAKE SWORD` - Pick up items
- `INVENTORY` - Check what you're carrying
- `HELP` - See all commands

---

## 📚 Understanding the Configuration Files

Now that you've run the app, let's understand what makes it work:

### 1. `.env.example` - Environment Variables Template

**Location**: `backend/.env.example`

**What is it?** A template showing what configuration the app needs.

**What to do with it:**
```powershell
# Copy it to create your configuration file
cd backend
Copy-Item .env.example .env

# Edit .env if you want to change settings
notepad .env
```

**What's inside:**
```dotenv
# Database connection info
DATABASE_URL=postgresql://wizard:wizard123@localhost:5432/wizards_keep

# App settings
DEBUG=true              # Show detailed errors (helpful for learning!)
LOG_LEVEL=INFO          # How much logging to show

# Security settings
SECRET_KEY=your-secret-key-here  # Change this in production!
```

**Key point**: `.env` files store configuration that might change between environments (development vs production) or contain secrets (passwords, keys).

**Read more**: [Configuration Guide](CONFIGURATION.md) explains every variable in detail.

---

### 2. `requirements.txt` - Python Dependencies

**Location**: `backend/requirements.txt`

**What is it?** Lists all Python packages the app needs to run.

**What's inside:**
```txt
fastapi==0.109.0        # Web framework
sqlalchemy==2.0.25      # Database ORM
psycopg2-binary==2.9.9  # PostgreSQL driver
pydantic==2.5.3         # Data validation
...
```

**Why two requirements files?**
- `requirements.txt` - Packages needed to **run** the app
- `requirements-dev.txt` - Additional packages for **development** (testing tools, debuggers, etc.)

**How to use:**
```powershell
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (includes production ones)
pip install -r requirements-dev.txt
```

**Read more**: [Configuration Guide](CONFIGURATION.md#python-dependencies) explains each package.

---

### 3. `docker-compose.yml` - Multi-Service Setup

**Location**: `docker-compose.yml` (project root)

**What is it?** Defines all the services (database, backend, frontend) and how they work together.

**Key sections:**
```yaml
services:
  database:       # PostgreSQL database
    image: postgres:15-alpine
    ports:
      - "5432:5432"
  
  backend:        # Python API
    build: ./backend
    ports:
      - "8000:8000"
  
  frontend:       # Web interface
    build: ./frontend
    ports:
      - "8080:80"
```

**Common commands:**
```powershell
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend

# Restart a service
docker-compose restart backend
```

**Read more**: [Configuration Guide](CONFIGURATION.md#docker-configuration) and [Docker Guide](DOCKER.md)

---

### 4. `pyproject.toml` - Tool Configuration

**Location**: `backend/pyproject.toml`

**What is it?** Configures development tools (code formatters, test runners, etc.)

**What's inside:**
```toml
[tool.black]              # Code formatter settings
line-length = 88

[tool.pytest.ini_options] # Test runner settings
testpaths = ["tests"]

[tool.mypy]               # Type checker settings
python_version = "3.11"
```

**Why this matters:** Ensures all developers use the same code style and testing setup.

**Read more**: [Configuration Guide](CONFIGURATION.md#python-configuration)

---

## 🧰 Understanding the Tools

Now let's understand what each technology does:

### Backend Technologies

#### FastAPI - Web Framework
**What is it?** A modern Python framework for building APIs (Application Programming Interfaces).

**Why we use it?**
- Fast to write code
- Automatically generates documentation
- Type-safe (catches errors early)

**Example:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
def say_hello():
    return {"message": "Hello, World!"}
```

Visit http://localhost:8000/hello and you'll see: `{"message": "Hello, World!"}`

**Learn more**: [Tools & Frameworks Guide - FastAPI](TOOLS_AND_FRAMEWORKS.md#fastapi)

---

#### SQLAlchemy - Object-Relational Mapper (ORM)
**What is it?** Lets you work with databases using Python code instead of SQL.

**Without ORM (raw SQL):**
```python
cursor.execute("SELECT * FROM players WHERE id = 1")
```

**With ORM (SQLAlchemy):**
```python
player = session.query(Player).filter(Player.id == 1).first()
```

**Why this matters:** More readable, safer (prevents SQL injection), and easier to maintain.

**Learn more**: [Tools & Frameworks Guide - SQLAlchemy ORM](TOOLS_AND_FRAMEWORKS.md#sqlalchemy-orm)

---

#### PostgreSQL - Database
**What is it?** A powerful database that stores all game data (players, locations, items).

**Why we use it:** 
- Reliable (won't lose your data)
- Supports relationships (players have inventories, locations connect to each other)
- Industry-standard (used by Netflix, Instagram, Reddit)

**What's stored:**
- Player accounts and character names
- Game state (location, health, inventory)
- World data (locations, items, enemies)

**Learn more**: [Tools & Frameworks Guide - PostgreSQL](TOOLS_AND_FRAMEWORKS.md#postgresql)

---

### Frontend Technologies

#### HTML - Structure
**What is it?** Defines the structure of web pages.

**Example from our game:**
```html
<div class="output" id="output">
    <!-- Game messages appear here -->
</div>
<input type="text" id="commandInput" placeholder="Enter command...">
```

---

#### CSS - Styling
**What is it?** Makes web pages look good (colors, fonts, layout).

**Example from our game:**
```css
body {
    background-color: #352879;  /* Commodore 64 blue */
    color: #33ff33;             /* Terminal green */
    font-family: 'Courier New'; /* Monospace font */
}
```

---

#### JavaScript - Behavior
**What is it?** Makes web pages interactive.

**Example from our game:**
```javascript
// When user presses Enter, send command to backend
async function executeCommand(command) {
    const response = await fetch('/api/v1/game/command', {
        method: 'POST',
        body: JSON.stringify({ command: command })
    });
    const result = await response.json();
    displayMessage(result.message);
}
```

**Learn more**: [Tools & Frameworks Guide - Frontend](TOOLS_AND_FRAMEWORKS.md#frontend)

---

### Development Tools

#### Docker - Containerization
**What is it?** Packages your application and all its dependencies into a "container" that runs anywhere.

**Analogy:** Like a shipping container - same package works on trucks, trains, ships, planes.

**Why we use it:**
- "Works on my machine" → "Works everywhere"
- Easy setup (one command to start everything)
- Isolated (won't conflict with other apps)

**Learn more**: [Docker Guide](DOCKER.md) and [Tools & Frameworks Guide - Docker](TOOLS_AND_FRAMEWORKS.md#docker)

---

#### pytest - Testing
**What is it?** Framework for writing automated tests.

**Example test:**
```python
def test_create_player():
    response = client.post("/api/v1/players/", 
        json={"username": "testuser", "character_name": "Test Hero"})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

**Why testing matters:** Ensures your code works correctly and catches bugs early.

**Learn more**: [Tools & Frameworks Guide - pytest](TOOLS_AND_FRAMEWORKS.md#pytest)

---

## 🎓 Your Learning Path

Now that you understand the basics, here's how to learn progressively:

### Week 1: Get Comfortable
- [ ] Run the application with Docker Compose
- [ ] Play the game, try all commands
- [ ] Explore the API documentation: http://localhost:8000/docs
- [ ] Read the [Quick Start Guide](QUICKSTART.md)

### Week 2: Understand the Technologies
- [ ] Read [Tools & Frameworks Guide](TOOLS_AND_FRAMEWORKS.md)
  - Focus on FastAPI, SQLAlchemy, PostgreSQL first
  - Then Docker, pytest, and code quality tools
- [ ] Read [Configuration Guide](CONFIGURATION.md)
  - Understand `.env` files
  - Learn about requirements files
  - Explore `docker-compose.yml`

### Week 3: Explore the Code
- [ ] Open `backend/app/main.py` - See how FastAPI works
- [ ] Read `backend/app/models/models.py` - Understand database models
- [ ] Study `backend/app/services/game_engine.py` - Game logic
- [ ] Look at `frontend/js/game.js` - Frontend code

### Week 4: Make Changes
- [ ] Add a new location to the game
- [ ] Create a new item or enemy
- [ ] Customize the UI colors
- [ ] Try adding a new command

### Week 5: Learn Testing
- [ ] Read tests in `backend/tests/`
- [ ] Run tests: `.\scripts\test.ps1`
- [ ] Write a test for your new feature
- [ ] Check test coverage

### Week 6: Master Docker
- [ ] Read [Docker Guide](DOCKER.md)
- [ ] Understand `Dockerfile.backend`
- [ ] Study `docker-compose.yml`
- [ ] Try modifying Docker configs

### Week 7+: Advanced Topics
- [ ] Study [Architecture Guide](ARCHITECTURE.md)
- [ ] Learn Kubernetes
- [ ] Explore CI/CD with GitHub Actions
- [ ] Contribute back to the project!

---

## 🆘 Common Questions

### Q: I get "permission denied" errors
**A:** On Windows, run PowerShell as Administrator. On Mac/Linux, use `sudo` for Docker commands.

### Q: Port 8080 is already in use
**A:** Change the port in `docker-compose.yml`:
```yaml
frontend:
  ports:
    - "8081:80"  # Use port 8081 instead
```

### Q: Database won't start
**A:** Make sure Docker is running (check system tray), then:
```powershell
docker-compose down
docker-compose up -d
```

### Q: I modified code but nothing changed
**A:** Rebuild the Docker image:
```powershell
docker-compose build backend
docker-compose up -d backend
```

### Q: Where are the database files stored?
**A:** In a Docker volume. View with:
```powershell
docker volume ls
docker volume inspect wizards-keep_postgres_data
```

### Q: How do I reset the database?
**A:**
```powershell
docker-compose down -v  # Delete volumes
docker-compose up -d
docker-compose exec backend python scripts/init_db.py
```

---

## 📖 Documentation Index

| Document | What You'll Learn |
|----------|------------------|
| [Quick Start](QUICKSTART.md) | Get running in 5 minutes |
| [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md) | Understand every technology |
| [Configuration](CONFIGURATION.md) | Master config files |
| [Architecture](ARCHITECTURE.md) | 3-tier design patterns |
| [API Reference](API.md) | REST API endpoints |
| [Docker Guide](DOCKER.md) | Containerization concepts |
| [Contributing](CONTRIBUTING.md) | Code standards & workflow |

---

## 💪 Next Steps

1. **Run the app**: `docker-compose up -d`
2. **Play the game**: http://localhost:8080
3. **Explore the API**: http://localhost:8000/docs
4. **Read the guides**: Start with [Tools & Frameworks](TOOLS_AND_FRAMEWORKS.md)
5. **Join the community**: Ask questions, share what you learned!

---

## 🎉 Welcome to Your Learning Journey!

Remember:
- 🐢 **Take your time** - Learning is a journey, not a race
- 🔨 **Break things** - That's how you learn! (You can always reset)
- ❓ **Ask questions** - Open GitHub issues with questions
- 🤝 **Help others** - Teaching reinforces learning
- 🎯 **Have fun** - You're building a game while learning!

**Happy coding and happy adventuring! 🗡️🛡️✨**
