# The Wizard's Keep

[![CI/CD Pipeline](https://github.com/andystumph/the-wizards-keep/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/andystumph/the-wizards-keep/actions/workflows/ci-cd.yml)

A text-based adventure game built to teach modern software development practices.

> **🎓 New to programming?** Start with our [Complete Beginner's Guide](docs/GETTING_STARTED.md) that explains everything from scratch!
> 
> **📚 Not sure where to start?** Check the [Documentation Index](docs/README.md) for guided learning paths!

## 🎮 Game Overview

**The Wizard's Keep** is a single-player text-based adventure game inspired by classic titles like Zork (1977). You play as a half-elven Ranger on a quest to infiltrate the Wizard's Keep and defeat the dark wizard who threatens the realm.

### Your Character: The Ranger

You are Kael Thornwind, a half-elven Ranger who has lived on the edges of civilization for most of your life. Raised by your elven mother in the deep forests, you learned the ancient art of tracking, the whisper-speak of animals, and the deadly precision of bow and blade. When your village was destroyed by the Wizard's dark magic, you swore an oath of vengeance. Now, you stand before the entrance to the Wizard's Keep, ready to face whatever horrors lie within.

### Game Features

- **3 Progressive Levels**: Journey from the Keep's entrance through increasingly dangerous areas
- **Text Command Interface**: Use commands like `LOOK AROUND`, `GO NORTH`, `PICK UP SWORD`, `ATTACK ORC`
- **Combat System**: Face orcs, goblins, kobolds, trolls, gnolls, hobgoblins, and the Wizard himself
- **Magic Items**: Discover powerful artifacts to aid in your quest
- **Boss Battles**: Each level culminates in a challenging encounter
- **Persistent Progress**: Your game state is saved in a PostgreSQL database

## 🎓 Educational Purpose

This project is designed as a **comprehensive learning resource** for developers who want to understand:

1. **3-Tier Architecture**: Separation of presentation, logic, and data layers
2. **RESTful API Design**: Building scalable backend services with FastAPI
3. **Database Design**: Schema design, migrations, and ORM usage with SQLAlchemy
4. **Containerization**: Docker and Docker Compose for local development
5. **Orchestration**: Kubernetes deployment patterns
6. **Testing**: Unit tests, integration tests, and test-driven development
7. **CI/CD**: Automated testing and deployment with GitHub Actions
8. **Code Quality**: Linting, formatting, and security scanning
9. **Modern Python**: Type hints, async/await, and best practices

### 📚 Learning Resources

**Start Here:**
- **[Complete Beginner's Guide](docs/GETTING_STARTED.md)** - Start here if you're new! Explains everything from prerequisites to advanced topics
- **[Quick Start Guide](docs/QUICKSTART.md)** - Get up and running in 5 minutes

**Understand the Stack:**
- **[Tools & Frameworks Guide](docs/TOOLS_AND_FRAMEWORKS.md)** - What is FastAPI? SQLAlchemy? Docker? Complete explanations of every tool
- **[Configuration Guide](docs/CONFIGURATION.md)** - What is .env.example for? What are requirements files? How does everything work?
- **[Testing Guide](docs/TESTING.md)** - Why test? How to write tests? Understanding pytest, fixtures, and coverage

**Deep Dives:**
- **[Architecture Guide](docs/ARCHITECTURE.md)** - 3-tier architecture patterns and design decisions
- **[API Reference](docs/API.md)** - Complete REST API documentation with examples
- **[Docker Guide](docs/DOCKER.md)** - Containerization concepts, best practices, and troubleshooting

**Contributing:**
- **[Contributing Guide](docs/CONTRIBUTING.md)** - Code standards, development workflow, and how to contribute

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     Frontend (Tier 1)                        │
│                HTML + CSS + JavaScript                       │
│             Retro terminal-style interface                   │
└──────────────────────────────────────────────────────────────┘
                           ↕ HTTP/REST
┌──────────────────────────────────────────────────────────────┐
│                   Backend API (Tier 2)                       │
│              FastAPI + Python 3.11+                          │
│          Game engine and business logic                      │
└──────────────────────────────────────────────────────────────┘
                            ↕ SQL
┌──────────────────────────────────────────────────────────────┐
│                    Database (Tier 3)                         │
│                   PostgreSQL 15+                             │
│      Game state, player data, world content                  │
└──────────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- Docker Desktop or Rancher Desktop
- Git

### Option 1: Docker Compose (Recommended for beginners)

```powershell
# Clone the repository
git clone https://github.com/yourusername/the-wizards-keep.git
cd the-wizards-keep

# Start all services
docker-compose up -d

# Initialize the database
docker-compose exec backend python -m scripts.init_db
```

Visit `http://localhost:8080` to play!

### Option 2: Local Development

```powershell
# Run the setup script
.\scripts\setup.ps1

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start PostgreSQL (via Docker)
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=wizard123 -e POSTGRES_DB=wizards_keep postgres:15

# Run database migrations
cd backend
python -m alembic upgrade head

# Start the backend
python -m uvicorn app.main:app --reload

# In a new terminal, start the frontend
cd frontend
python -m http.server 8080
```

### Option 3: Kubernetes

```powershell
# Deploy to Kubernetes cluster
kubectl apply -f k8s/

# Wait for pods to be ready
kubectl wait --for=condition=ready pod -l app=wizards-keep --timeout=120s

# Port forward to access
kubectl port-forward service/frontend 8080:80
```

## 📖 Documentation

Comprehensive documentation is available in the `docs/` directory:

- **[Architecture Guide](docs/ARCHITECTURE.md)**: Deep dive into the 3-tier design
- **[API Reference](docs/API.md)**: Complete REST API documentation
- **[Database Schema](docs/DATABASE.md)**: Tables, relationships, and design decisions
- **[Game Design](docs/GAME_DESIGN.md)**: Story, levels, items, and enemies
- **[Docker Guide](docs/DOCKER.md)**: Containerization explained
- **[Kubernetes Guide](docs/KUBERNETES.md)**: K8s deployment patterns
- **[Testing Guide](docs/TESTING.md)**: How to write and run tests
- **[Contributing](docs/CONTRIBUTING.md)**: How to contribute to the project

## 🧪 Testing

```powershell
# Run all tests
.\scripts\test.ps1

# Run with coverage
pytest --cov=backend --cov-report=html

# Run linting
.\scripts\lint.ps1

# Run security scan
bandit -r backend/
```

## 📝 Game Commands

- **Movement**: `GO NORTH`, `GO SOUTH`, `GO EAST`, `GO WEST`, `GO UP`, `GO DOWN`
- **Observation**: `LOOK`, `LOOK AROUND`, `EXAMINE [ITEM]`, `INVENTORY`
- **Interaction**: `TAKE [ITEM]`, `DROP [ITEM]`, `USE [ITEM]`
- **Combat**: `ATTACK [ENEMY]`, `FLEE`
- **Communication**: `TALK TO [CREATURE]`, `SPEAK [LANGUAGE]`
- **System**: `HELP`, `SAVE`, `QUIT`, `STATS`

## 🛠️ Technology Stack

**Frontend:**
- HTML5 / CSS3
- Vanilla JavaScript (ES6+)
- No framework (educational simplicity)

**Backend:**
- Python 3.11+
- FastAPI (modern async web framework)
- SQLAlchemy (ORM)
- Alembic (database migrations)
- Pydantic (data validation)

**Database:**
- PostgreSQL 15+

**DevOps:**
- Docker & Docker Compose
- Kubernetes
- GitHub Actions
- pytest, black, flake8, mypy, bandit

## 📊 Project Structure

```
the-wizards-keep/
├── backend/                 # Tier 2: API and game logic
│   ├── app/
│   │   ├── api/            # REST endpoints
│   │   ├── core/           # Configuration
│   │   ├── models/         # Database models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   └── main.py         # FastAPI application
│   ├── tests/              # Unit and integration tests
│   ├── alembic/            # Database migrations
│   └── requirements.txt
├── frontend/               # Tier 1: User interface
│   ├── index.html
│   ├── css/
│   ├── js/
│   └── assets/
├── database/               # Tier 3: Database configs
│   └── init/
├── k8s/                    # Kubernetes manifests
├── scripts/                # Automation scripts
│   ├── setup.ps1           # Windows setup
│   ├── setup.sh            # Linux/Mac setup
│   ├── test.ps1
│   └── test.sh
├── docs/                   # Documentation
├── .github/
│   └── workflows/          # CI/CD pipelines
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
└── README.md
```

## 🎯 Learning Path

If you're new to these concepts, we recommend this progressive learning path:

### 1️⃣ Beginner: Get It Running
- ✅ Read [Quick Start Guide](docs/QUICKSTART.md)
- ✅ Run with Docker Compose: `docker-compose up -d`
- ✅ Play the game and explore commands
- ✅ View API docs: http://localhost:8000/docs

### 2️⃣ Understand the Tools
- ✅ Read [Tools & Frameworks Guide](docs/TOOLS_AND_FRAMEWORKS.md)
  - Learn what FastAPI, SQLAlchemy, PostgreSQL, Docker, etc. are
  - Understand why we chose each technology
- ✅ Read [Configuration Guide](docs/CONFIGURATION.md)
  - Understand `.env.example` and environment variables
  - Learn the difference between `requirements.txt` and `requirements-dev.txt`
  - Explore `pyproject.toml`, `setup.cfg`, and other config files

### 3️⃣ Explore the Code
- ✅ **Frontend**: Modify `frontend/index.html` and `frontend/css/style.css`
- ✅ **API**: Study `backend/app/api/v1/endpoints/` to understand REST APIs
- ✅ **Game Logic**: Read `backend/app/services/game_engine.py`
- ✅ **Database**: Examine `backend/app/models/models.py` (SQLAlchemy ORM)

### 4️⃣ Make Changes
- ✅ Add a new location to the game (`backend/scripts/init_db.py`)
- ✅ Create a new item or enemy
- ✅ Add a new command to the game engine
- ✅ Customize the UI styling

### 5️⃣ Testing & Quality
- ✅ Read [Testing Guide](docs/TESTING.md) to understand testing fundamentals
- ✅ Study test examples in `backend/tests/`
- ✅ Write a test for your new feature
- ✅ Run tests: `.\scripts\test.ps1`
- ✅ Check coverage: `pytest --cov=app --cov-report=html`
- ✅ Run linters: `black`, `flake8`, `mypy`

### 6️⃣ Containerization
- ✅ Read [Docker Guide](docs/DOCKER.md)
- ✅ Understand `Dockerfile.backend` (multi-stage builds)
- ✅ Study `docker-compose.yml` (multi-container orchestration)
- ✅ Learn about volumes, networks, and health checks

### 7️⃣ Advanced: Kubernetes
- ✅ Read [Architecture Guide](docs/ARCHITECTURE.md)
- ✅ Explore `k8s/*.yaml` manifests
- ✅ Deploy locally: `kubectl apply -f k8s/`
- ✅ Understand Deployments, Services, ConfigMaps, Secrets

### 8️⃣ Professional: CI/CD
- ✅ Study `.github/workflows/ci-cd.yml`
- ✅ Understand automated testing and building
- ✅ Learn about GitHub Actions jobs and steps

## 🤝 Contributing

This is an educational project, and contributions are welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- Inspired by Zork (1977) by Infocom
- Classic D&D mechanics
- Modern web development practices

## 📧 Contact

Questions? Open an issue or start a discussion!

---

**Remember**: This project is about learning. Take your time, read the code, experiment, and break things. That's how we grow as developers! 🚀
