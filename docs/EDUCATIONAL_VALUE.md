# Educational Value Map

A guide showing what you'll learn from each file in this project.

## 🎓 Learning Outcomes by File

### Backend Files

#### `backend/app/main.py`
**What you'll learn:**
- ✅ FastAPI application structure
- ✅ CORS (Cross-Origin Resource Sharing) configuration
- ✅ Application lifecycle management (startup/shutdown)
- ✅ Global exception handling
- ✅ API versioning patterns
- ✅ Middleware setup

**Key concepts:**
```python
# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    yield
    # Shutdown logic

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(...)
```

---

#### `backend/app/models/models.py`
**What you'll learn:**
- ✅ SQLAlchemy ORM (Object-Relational Mapping)
- ✅ Database schema design
- ✅ Table relationships (one-to-many, many-to-many)
- ✅ Foreign keys and indexes
- ✅ Enums in databases
- ✅ Timestamps and default values

**Key concepts:**
```python
# Relationship definition
class Player(Base):
    game_state = relationship("GameState", back_populates="player")

# Foreign key
class GameState(Base):
    player_id = Column(Integer, ForeignKey("players.id"))
```

---

#### `backend/app/schemas/schemas.py`
**What you'll learn:**
- ✅ Pydantic models for validation
- ✅ Type hints and type safety
- ✅ Request/response data structures
- ✅ Validation rules
- ✅ Model configuration

**Key concepts:**
```python
# Validation with Pydantic
class PlayerCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    character_name: str = Field(..., max_length=100)
```

---

#### `backend/app/core/database.py`
**What you'll learn:**
- ✅ Database connection management
- ✅ Connection pooling
- ✅ Session management
- ✅ Dependency injection pattern
- ✅ Context managers

**Key concepts:**
```python
# Dependency injection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

#### `backend/app/core/config.py`
**What you'll learn:**
- ✅ Configuration management
- ✅ Environment variables
- ✅ Pydantic settings
- ✅ Type-safe configuration
- ✅ Default values

**Key concepts:**
```python
# Type-safe configuration
class Settings(BaseSettings):
    DATABASE_URL: str
    DEBUG: bool = False
    
    class Config:
        env_file = ".env"
```

---

#### `backend/app/services/game_engine.py`
**What you'll learn:**
- ✅ Business logic separation
- ✅ Command pattern implementation
- ✅ Regular expressions for parsing
- ✅ State management
- ✅ Game mechanics
- ✅ Error handling

**Key concepts:**
```python
# Command pattern
def process_command(self, command: str, player_id: int):
    if re.match(r'^GO (NORTH|SOUTH|EAST|WEST)', command):
        return self._handle_move(...)
    elif re.match(r'^ATTACK (.+)', command):
        return self._handle_attack(...)
```

---

#### `backend/app/api/v1/endpoints/*.py`
**What you'll learn:**
- ✅ REST API design
- ✅ HTTP methods (GET, POST, PUT, DELETE)
- ✅ Status codes (200, 201, 404, etc.)
- ✅ Request/response handling
- ✅ Error responses
- ✅ API documentation with docstrings

**Key concepts:**
```python
@router.post("/", response_model=PlayerResponse, status_code=201)
async def create_player(
    player: PlayerCreate,
    db: Session = Depends(get_db)
):
    """Create a new player."""
```

---

### Frontend Files

#### `frontend/index.html`
**What you'll learn:**
- ✅ HTML5 semantic structure
- ✅ Form handling
- ✅ Single-page application layout
- ✅ Accessibility attributes
- ✅ Screen management (multiple views)

**Key concepts:**
```html
<!-- Semantic HTML -->
<section id="welcomeScreen">
    <form id="characterForm">
        <input type="text" required>
    </form>
</section>
```

---

#### `frontend/css/style.css`
**What you'll learn:**
- ✅ CSS custom properties (variables)
- ✅ Flexbox layout
- ✅ Responsive design
- ✅ Animations and transitions
- ✅ Custom scrollbar styling
- ✅ Retro/theme design

**Key concepts:**
```css
/* CSS Variables */
:root {
    --primary-color: #352879;
    --text-color: #33ff33;
}

/* Flexbox */
.container {
    display: flex;
    flex-direction: column;
}
```

---

#### `frontend/js/config.js`
**What you'll learn:**
- ✅ Configuration module pattern
- ✅ Environment-based config
- ✅ Constants management

---

#### `frontend/js/api.js`
**What you'll learn:**
- ✅ Fetch API for HTTP requests
- ✅ Async/await syntax
- ✅ Error handling in JavaScript
- ✅ JSON parsing
- ✅ API client pattern

**Key concepts:**
```javascript
async function createPlayer(username, characterName) {
    const response = await fetch(`${API_URL}/players/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, character_name: characterName })
    });
    if (!response.ok) throw new Error('API error');
    return await response.json();
}
```

---

#### `frontend/js/game.js`
**What you'll learn:**
- ✅ Client-side state management
- ✅ DOM manipulation
- ✅ Event handling
- ✅ Module pattern
- ✅ Command history (like terminal)

**Key concepts:**
```javascript
// State management
const Game = {
    currentPlayer: null,
    commandHistory: [],
    historyIndex: -1,
    
    updateGameState(state) {
        // Update UI with new state
    }
};
```

---

#### `frontend/js/main.js`
**What you'll learn:**
- ✅ Application initialization
- ✅ Event binding
- ✅ Screen transitions
- ✅ Form validation
- ✅ Error handling

---

### Configuration Files

#### `backend/.env.example`
**What you'll learn:**
- ✅ Environment variable patterns
- ✅ Secret management
- ✅ Configuration separation
- ✅ Security best practices

**Educational value:**
- Shows what configuration is needed
- Documents expected values
- Demonstrates dev vs production differences

---

#### `backend/requirements.txt`
**What you'll learn:**
- ✅ Python dependency management
- ✅ Version pinning
- ✅ Semantic versioning
- ✅ Dependency conflicts

**Educational value:**
- See production dependencies
- Understand package ecosystem
- Learn about version constraints

---

#### `backend/requirements-dev.txt`
**What you'll learn:**
- ✅ Development vs production dependencies
- ✅ Development tools ecosystem
- ✅ The `-r` directive for including other files

**Educational value:**
- Understand testing tools
- Learn about code quality tools
- See debugging tools

---

#### `backend/pyproject.toml`
**What you'll learn:**
- ✅ Modern Python project configuration (PEP 518)
- ✅ Tool configuration (black, pytest, mypy)
- ✅ TOML format
- ✅ Consistent team settings

**Educational value:**
- How to configure multiple tools
- Why consistency matters
- Modern Python standards

---

#### `backend/setup.cfg`
**What you'll learn:**
- ✅ Legacy Python configuration
- ✅ INI file format
- ✅ Tool compatibility

---

### Docker Files

#### `Dockerfile.backend`
**What you'll learn:**
- ✅ Docker image creation
- ✅ Multi-stage builds
- ✅ Layer caching optimization
- ✅ Security (non-root user)
- ✅ Health checks

**Key concepts:**
```dockerfile
# Multi-stage build
FROM python:3.11-slim as builder
RUN pip install -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib /usr/local/lib
```

**Educational value:**
- Containerization basics
- Image size optimization (500MB → 250MB)
- Security best practices

---

#### `Dockerfile.frontend`
**What you'll learn:**
- ✅ Static file serving
- ✅ Nginx configuration
- ✅ Production builds

---

#### `docker-compose.yml`
**What you'll learn:**
- ✅ Multi-container orchestration
- ✅ Service dependencies (`depends_on`)
- ✅ Health checks
- ✅ Volume management
- ✅ Network creation
- ✅ Environment variables

**Key concepts:**
```yaml
services:
  backend:
    depends_on:
      database:
        condition: service_healthy
```

**Educational value:**
- How services communicate
- Data persistence with volumes
- Service startup order
- Development vs production setups

---

#### `.dockerignore`
**What you'll learn:**
- ✅ Build context optimization
- ✅ Security (excluding secrets)
- ✅ Image size reduction

---

### Kubernetes Files

#### `k8s/01-namespace.yaml`
**What you'll learn:**
- ✅ Kubernetes namespaces
- ✅ Resource isolation
- ✅ YAML structure

---

#### `k8s/02-configmap.yaml`
**What you'll learn:**
- ✅ Non-secret configuration
- ✅ Environment variable injection
- ✅ Configuration separation

---

#### `k8s/03-secrets.yaml`
**What you'll learn:**
- ✅ Secret management
- ✅ Base64 encoding
- ✅ Secret references

---

#### `k8s/04-pvc.yaml`
**What you'll learn:**
- ✅ Persistent storage
- ✅ Volume claims
- ✅ Storage classes

---

#### `k8s/*-deployment.yaml`
**What you'll learn:**
- ✅ Pod specifications
- ✅ Replica management
- ✅ Resource limits
- ✅ Environment variables from ConfigMaps/Secrets
- ✅ Volume mounts
- ✅ Health probes (liveness, readiness)

**Key concepts:**
```yaml
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: backend
        resources:
          limits:
            memory: "512Mi"
            cpu: "500m"
```

**Educational value:**
- Container orchestration
- Scaling strategies
- Resource management
- High availability

---

#### `k8s/*-service.yaml`
**What you'll learn:**
- ✅ Service types (ClusterIP, LoadBalancer)
- ✅ Service discovery
- ✅ Internal DNS
- ✅ Load balancing

---

### Testing Files

#### `backend/tests/conftest.py`
**What you'll learn:**
- ✅ Pytest fixtures
- ✅ Test setup/teardown
- ✅ Database isolation (test DB)
- ✅ Dependency overrides
- ✅ Test client setup

**Key concepts:**
```python
@pytest.fixture
def test_db():
    # Setup: Create test database
    yield db
    # Teardown: Clean up
```

**Educational value:**
- Test isolation
- Fixture patterns
- Test database management

---

#### `backend/tests/test_api.py`
**What you'll learn:**
- ✅ API testing
- ✅ HTTP request testing
- ✅ Response validation
- ✅ Status code testing
- ✅ Test organization

**Key concepts:**
```python
def test_create_player(client):
    response = client.post("/api/v1/players/", json={...})
    assert response.status_code == 201
    assert response.json()["username"] == "testuser"
```

---

#### `backend/tests/test_game_engine.py`
**What you'll learn:**
- ✅ Unit testing
- ✅ Business logic testing
- ✅ Mock objects
- ✅ Test data creation

---

### CI/CD Files

#### `.github/workflows/ci-cd.yml`
**What you'll learn:**
- ✅ GitHub Actions
- ✅ Workflow syntax
- ✅ Job dependencies
- ✅ Matrix testing (multiple Python versions)
- ✅ Service containers (PostgreSQL)
- ✅ Artifact building
- ✅ Security scanning

**Key concepts:**
```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    services:
      postgres:
        image: postgres:15
```

**Educational value:**
- Automated testing
- Continuous integration
- Build automation
- Security in CI/CD

---

### Scripts

#### `scripts/setup.ps1` and `scripts/setup.sh`
**What you'll learn:**
- ✅ PowerShell scripting (Windows)
- ✅ Bash scripting (Linux/Mac)
- ✅ Cross-platform automation
- ✅ Virtual environment setup
- ✅ Error handling in scripts

---

#### `scripts/test.ps1` and `scripts/test.sh`
**What you'll learn:**
- ✅ Test automation
- ✅ Coverage reporting
- ✅ Script parameters
- ✅ Exit codes

---

#### `backend/scripts/init_db.py`
**What you'll learn:**
- ✅ Database seeding
- ✅ Data initialization
- ✅ Bulk inserts
- ✅ Game world design

**Educational value:**
- How to populate a database
- Game content structure
- Data relationships

---

## 🎯 Learning by File Type

### Want to learn Backend Development?
**Start with these files:**
1. `backend/app/main.py` - Application structure
2. `backend/app/models/models.py` - Database models
3. `backend/app/api/v1/endpoints/players.py` - Simple API
4. `backend/app/services/game_engine.py` - Business logic
5. `backend/tests/test_api.py` - Testing

---

### Want to learn Frontend Development?
**Start with these files:**
1. `frontend/index.html` - HTML structure
2. `frontend/css/style.css` - Styling
3. `frontend/js/config.js` - Configuration
4. `frontend/js/api.js` - API calls
5. `frontend/js/game.js` - State management

---

### Want to learn DevOps?
**Start with these files:**
1. `docker-compose.yml` - Local development
2. `Dockerfile.backend` - Container images
3. `k8s/05-database-deployment.yaml` - Kubernetes basics
4. `k8s/06-database-service.yaml` - Services
5. `.github/workflows/ci-cd.yml` - CI/CD

---

### Want to learn Testing?
**Start with these files:**
1. **[Testing Guide](TESTING.md)** - Read this comprehensive guide first!
2. `backend/tests/conftest.py` - Test setup and fixtures
3. `backend/tests/test_api.py` - Integration test examples
4. `backend/tests/test_game_engine.py` - Unit test examples
5. `pyproject.toml` - Test configuration

---

### Want to learn Configuration Management?
**Start with these files:**
1. `backend/.env.example` - Environment variables
2. `backend/requirements.txt` - Dependencies
3. `backend/pyproject.toml` - Tool config
4. `docker-compose.yml` - Service config

---

## 📊 Complexity Levels

### 🟢 Beginner-Friendly
- `frontend/index.html` - Basic HTML
- `frontend/css/style.css` - Basic CSS
- `backend/.env.example` - Configuration
- `backend/requirements.txt` - Dependencies
- `docker-compose.yml` - Basic concepts

### 🟡 Intermediate
- `backend/app/main.py` - FastAPI basics
- `backend/app/models/models.py` - ORM
- `frontend/js/game.js` - JavaScript patterns
- `Dockerfile.backend` - Container basics
- `backend/tests/test_api.py` - Testing

### 🔴 Advanced
- `backend/app/services/game_engine.py` - Complex logic
- `k8s/*.yaml` - Kubernetes orchestration
- `.github/workflows/ci-cd.yml` - CI/CD
- `backend/app/core/database.py` - Connection management

---

## 🎓 Progressive Learning Path

### Level 1: Run and Observe
**Focus:** Get it working, see how pieces connect
- Run with `docker-compose up -d`
- Play the game
- View API docs at http://localhost:8000/docs
- Look at files, don't worry about understanding everything

### Level 2: Understand Structure
**Focus:** Learn what each file does
- Read this Educational Value Map
- Open files and read comments
- Follow request/response flow
- Understand the 3 tiers

### Level 3: Make Small Changes
**Focus:** Modify existing code
- Change UI colors in `style.css`
- Add a location in `init_db.py`
- Modify API response in `endpoints/players.py`
- Run tests to ensure nothing broke

### Level 4: Add Features
**Focus:** Create new functionality
- Add a new command to game engine
- Create a new API endpoint
- Add a new database model
- Write tests for your changes

### Level 5: Understand Architecture
**Focus:** See the big picture
- Study [Architecture Guide](ARCHITECTURE.md)
- Understand design patterns used
- Learn why decisions were made
- Consider alternatives

### Level 6: Master DevOps
**Focus:** Deployment and operations
- Build custom Docker images
- Deploy to Kubernetes
- Set up CI/CD
- Monitor and scale

---

## 💡 Tips for Learning

1. **Read Comments**: Every file has educational comments
2. **Follow Patterns**: See something done once? Look for similar patterns
3. **Break Things**: Copy the project and experiment
4. **Use Debuggers**: Set breakpoints and step through code
5. **Read Docs**: Follow links to official documentation
6. **Ask Questions**: Open GitHub issues
7. **Teach Others**: Best way to solidify learning

---

## 🎯 Practical Exercises

### Exercise 1: Add a New Item
**Files to modify:**
- `backend/scripts/init_db.py`

**What you'll learn:** Database seeding, game balance

---

### Exercise 2: Add a New API Endpoint
**Files to modify:**
- `backend/app/api/v1/endpoints/*.py`
- `backend/app/schemas/schemas.py`

**What you'll learn:** REST API design, Pydantic validation

---

### Exercise 3: Customize the UI
**Files to modify:**
- `frontend/css/style.css`
- `frontend/index.html`

**What you'll learn:** CSS, HTML, theming

---

### Exercise 4: Add a New Command
**Files to modify:**
- `backend/app/services/game_engine.py`

**What you'll learn:** Command pattern, regex, game logic

---

### Exercise 5: Write a Test
**Files to modify:**
- `backend/tests/test_api.py` or create new test file

**What you'll learn:** Test-driven development, pytest

---

## 📚 Next Steps

1. **Choose your focus area** (backend, frontend, devops)
2. **Start with beginner files** in that area
3. **Read the relevant documentation guides**
4. **Make small changes and test**
5. **Gradually tackle more complex files**
6. **Contribute back to the project!**

---

**Remember:** Every expert was once a beginner. Take your time, be patient with yourself, and enjoy the journey! 🚀
