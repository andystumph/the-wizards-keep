# Quick Start Guide

Get The Wizard's Keep up and running in minutes!

## Prerequisites

Before you begin, ensure you have:
- ✅ **Python 3.11+** ([Download](https://www.python.org/downloads/))
- ✅ **Docker Desktop** or **Rancher Desktop** ([Download](https://www.docker.com/products/docker-desktop/) | [Rancher](https://rancherdesktop.io/))
- ✅ **Git** (optional but recommended) ([Download](https://git-scm.com/downloads))

Check your installations:
```powershell
python --version   # Should show Python 3.11 or higher
docker --version   # Should show Docker version
```

## Installation

### Option 1: Quick Start with Docker Compose (Recommended)

The easiest way to run the entire application:

```powershell
# 1. Clone or download the project
git clone https://github.com/yourusername/the-wizards-keep.git
cd the-wizards-keep

# 2. Start everything with one command
docker-compose up -d

# 3. Initialize the database
docker-compose exec backend python scripts/init_db.py

# 4. Open your browser
start http://localhost:8080
```

That's it! The game is now running.

**What just happened?**
- PostgreSQL database started on port 5432
- Backend API started on port 8000
- Frontend web server started on port 8080
- Game world populated with locations, items, and enemies

---

### Option 2: Local Development Setup

For active development and debugging:

```powershell
# 1. Clone the project
git clone https://github.com/yourusername/the-wizards-keep.git
cd the-wizards-keep

# 2. Run the setup script
.\scripts\setup.ps1

# This script will:
# - Create Python virtual environment
# - Install dependencies
# - Start PostgreSQL in Docker
# - Initialize the database

# 3. Start the backend (in one terminal)
cd backend
python -m uvicorn app.main:app --reload

# 4. Start the frontend (in another terminal)
cd frontend
python -m http.server 8080

# 5. Open your browser
start http://localhost:8080
```

---

## Playing the Game

### Character Creation

1. Open http://localhost:8080
2. Enter a unique username
3. Enter your character name (or keep "Kael Thornwind")
4. Click "BEGIN YOUR QUEST"

### Basic Commands

Type commands in the input box and press Enter:

**Look around**:
```
LOOK
```

**Move**:
```
GO NORTH
GO SOUTH
GO EAST
GO WEST
```

**Check inventory**:
```
INVENTORY
```

**Pick up items**:
```
TAKE SWORD
TAKE POTION
```

**Use items**:
```
USE POTION
```

**Combat**:
```
ATTACK GOBLIN
FLEE
```

**Help**:
```
HELP
STATS
```

### Quick Tips

- 🗺️ Type `LOOK` when entering new areas to see exits and items
- 💼 Check your `INVENTORY` often
- ⚔️ Equip weapons for more damage
- 🧪 Use potions to restore health
- 📝 Type `HELP` anytime for a command list
- 💾 Your progress is automatically saved

---

## Stopping the Application

### Docker Compose
```powershell
docker-compose down
```

### Local Development
Press `Ctrl+C` in each terminal window.

To stop the database:
```powershell
docker stop wizards-keep-db
```

---

## Troubleshooting

### Can't access http://localhost:8080

**Problem**: Port might be in use.

**Solution**: Change the frontend port:
```powershell
cd frontend
python -m http.server 8081  # Use port 8081 instead
```

Then access http://localhost:8081

---

### Database connection error

**Problem**: PostgreSQL not running.

**Solution**: 
```powershell
# Check if container exists
docker ps -a | findstr wizards-keep-db

# If it exists but stopped
docker start wizards-keep-db

# If it doesn't exist
docker run -d --name wizards-keep-db `
  -p 5432:5432 `
  -e POSTGRES_USER=wizard `
  -e POSTGRES_PASSWORD=wizard123 `
  -e POSTGRES_DB=wizards_keep `
  postgres:15-alpine
```

---

### "Module not found" errors

**Problem**: Dependencies not installed.

**Solution**:
```powershell
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Install dependencies
cd backend
pip install -r requirements-dev.txt
```

---

### Docker won't start

**Problem**: Docker Desktop/Rancher Desktop not running.

**Solution**: Launch Docker Desktop or Rancher Desktop from your Start menu.

---

### Game database is empty

**Problem**: Database not initialized.

**Solution**:
```powershell
# For Docker Compose
docker-compose exec backend python scripts/init_db.py

# For local development
cd backend
python scripts/init_db.py
```

---

## Next Steps

Now that you have the game running, here's your learning journey:

### 🎮 First: Play the Game!
- Complete all 3 levels
- Defeat the three bosses
- Discover all items and locations
- Try all the commands

### 📚 Then: Learn the Technologies

**Essential Reading** (start here):
1. **[Tools & Frameworks Guide](TOOLS_AND_FRAMEWORKS.md)**
   - What is FastAPI? What is SQLAlchemy ORM?
   - Why do we use Docker? What is Kubernetes?
   - Complete explanations of every tool and technology
   - Learn by doing: includes examples and use cases

2. **[Configuration Guide](CONFIGURATION.md)**
   - What is `.env.example` for? (Answer: Copy it to `.env` and customize!)
   - What are `requirements.txt` vs `requirements-dev.txt`? (Answer: Production vs development dependencies)
   - How do all the config files work? (pyproject.toml, setup.cfg, docker-compose.yml, etc.)

### 🔍 Explore the Code

Start with these files:
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/services/game_engine.py` - Game command processing
- `backend/app/models/models.py` - Database schema (SQLAlchemy ORM)
- `frontend/js/game.js` - Frontend game logic
- `docker-compose.yml` - Multi-container setup

### 📖 Read the Documentation

- **[Architecture Guide](ARCHITECTURE.md)** - Understand the 3-tier design
- **[API Reference](API.md)** - Explore the REST API endpoints
- **[Docker Guide](DOCKER.md)** - Learn containerization concepts
- **[Contributing Guide](CONTRIBUTING.md)** - Code standards and workflow

### 🛠️ Make Your First Change

Easy modifications to try:
1. **Add a new item**: Edit `backend/scripts/init_db.py`
2. **Add a new location**: Extend the game world
3. **Create a new enemy**: Add to the bestiary
4. **Customize the UI**: Modify `frontend/css/style.css`
5. **Add a new command**: Extend `game_engine.py`

### ✅ Run Tests
```powershell
# Run all tests
.\scripts\test.ps1

# Run specific test file
pytest backend/tests/test_game_engine.py

# Run with coverage
pytest --cov=app --cov-report=html
```

### 🐳 Learn Docker
```powershell
# View running containers
docker ps

# View logs
docker-compose logs -f backend

# Rebuild after changes
docker-compose build backend
docker-compose up -d backend
```

### ☸️ Deploy to Kubernetes
```powershell
# Apply all manifests
kubectl apply -f k8s/

# Check status
kubectl get pods -n wizards-keep

# View logs
kubectl logs -n wizards-keep deployment/backend
```

---

## Common Workflows

### Reset the game
```powershell
# Via API
curl -X POST http://localhost:8000/api/v1/game/reset/1

# Or delete and recreate player via UI
```

### View API documentation
Open http://localhost:8000/docs

### View logs
```powershell
# Docker Compose
docker-compose logs -f backend

# Individual container
docker logs wizards-keep-backend
```

### Update game content
Edit `backend/scripts/init_db.py`, then:
```powershell
# Drop and recreate database
docker-compose down -v
docker-compose up -d
docker-compose exec backend python scripts/init_db.py
```

---

## Getting Help

- 📖 **Documentation**: Check the `docs/` folder
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/the-wizards-keep/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/yourusername/the-wizards-keep/discussions)
- 📧 **Questions**: Open an issue with the "question" label

---

## Happy Adventuring! 🗡️

May your blade stay sharp and your potions plentiful as you journey through The Wizard's Keep!
