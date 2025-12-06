# Testing Guide

A comprehensive guide to testing in The Wizard's Keep project.

## Table of Contents

- [Why Testing Matters](#why-testing-matters)
- [Types of Tests](#types-of-tests)
- [Testing Stack](#testing-stack)
- [Running Tests](#running-tests)
- [Writing Tests](#writing-tests)
- [Test Organization](#test-organization)
- [Test Coverage](#test-coverage)
- [Best Practices](#best-practices)
- [Common Patterns](#common-patterns)
- [Troubleshooting](#troubleshooting)

---

## Why Testing Matters

**"If it's not tested, it's broken."** - Ancient developer proverb

### Benefits of Testing

1. **Catch Bugs Early** 🐛
   - Find issues before users do
   - Cheaper to fix (minutes vs. hours/days)
   - Prevent regressions (old bugs coming back)

2. **Confidence to Refactor** 💪
   - Change code without fear
   - Tests ensure behavior stays correct
   - Improve code structure safely

3. **Living Documentation** 📚
   - Tests show how code should work
   - Better than comments (tests must stay current)
   - Examples of API usage

4. **Better Design** 🎨
   - Testable code is often better code
   - Forces you to think about interfaces
   - Reduces coupling between components

5. **Faster Development** 🚀
   - Seems slow at first, but saves time overall
   - No manual testing needed
   - Find issues immediately, not days later

### Real-World Example

**Without tests:**
```
1. Make a change
2. Manually test in browser
3. Check database
4. Test various scenarios
5. Deploy
6. User finds bug
7. Emergency fix
   Total time: Hours to days
```

**With tests:**
```
1. Make a change
2. Run tests (30 seconds)
3. All green? Deploy with confidence
   Total time: Minutes
```

---

## Types of Tests

### Unit Tests
**What:** Test individual functions/classes in isolation

**Example:**
```python
def test_calculate_damage():
    """Test damage calculation for weapon."""
    weapon = Item(name="Sword", damage=10)
    damage = calculate_damage(weapon, enemy_defense=5)
    assert damage == 5  # 10 damage - 5 defense
```

**When to use:**
- Testing business logic
- Testing calculations
- Testing data transformations

**Pros:**
- ✅ Fast (milliseconds)
- ✅ Easy to pinpoint failures
- ✅ Can test edge cases easily

**Cons:**
- ❌ Don't test integration between components
- ❌ May miss real-world issues

---

### Integration Tests
**What:** Test multiple components working together

**Example:**
```python
def test_create_player_and_start_game(client, db_session):
    """Test creating a player and starting a game."""
    # Create player
    response = client.post("/api/v1/players/", json={
        "username": "testuser",
        "character_name": "Test Hero"
    })
    player_id = response.json()["id"]
    
    # Start game (creates game_state)
    response = client.post("/api/v1/game/command", json={
        "player_id": player_id,
        "command": "LOOK"
    })
    assert response.status_code == 200
    assert "Forest Path" in response.json()["message"]
```

**When to use:**
- Testing API endpoints
- Testing database operations
- Testing service interactions

**Pros:**
- ✅ Tests realistic scenarios
- ✅ Catches integration bugs
- ✅ More confidence in overall system

**Cons:**
- ❌ Slower than unit tests
- ❌ Harder to debug failures
- ❌ More setup required

---

### End-to-End (E2E) Tests
**What:** Test the entire system from user's perspective

**Example (conceptual - we don't have E2E tests yet):**
```javascript
// Using a tool like Playwright or Selenium
test('complete game flow', async ({ page }) => {
  // Navigate to game
  await page.goto('http://localhost:8080');
  
  // Create character
  await page.fill('#username', 'testuser');
  await page.fill('#characterName', 'Test Hero');
  await page.click('#startButton');
  
  // Execute command
  await page.fill('#commandInput', 'LOOK');
  await page.press('#commandInput', 'Enter');
  
  // Verify output
  await expect(page.locator('#output')).toContainText('Forest Path');
});
```

**When to use:**
- Testing critical user workflows
- Testing frontend + backend + database together
- Pre-release verification

**Pros:**
- ✅ Tests exactly what users experience
- ✅ Catches UI bugs
- ✅ Maximum confidence

**Cons:**
- ❌ Slowest (seconds to minutes)
- ❌ Flaky (timing issues, network issues)
- ❌ Expensive to maintain

---

### Test Pyramid

```
        /\
       /E2E\      ← Few (10%)
      /------\
     /  INT   \   ← Some (30%)
    /----------\
   /    UNIT    \ ← Many (60%)
  /--------------\
```

**Rule of thumb:**
- 60% Unit tests (fast, focused)
- 30% Integration tests (realistic scenarios)
- 10% E2E tests (critical workflows only)

---

## Testing Stack

### pytest - Test Runner

**What it does:** Finds and runs tests, reports results

**Key features:**
- Simple syntax (`assert` instead of `assertEqual`)
- Powerful fixtures
- Parametrized tests
- Plugins for everything

**Installation:**
```powershell
pip install pytest
```

**Basic usage:**
```powershell
# Run all tests
pytest

# Run specific file
pytest backend/tests/test_api.py

# Run specific test
pytest backend/tests/test_api.py::test_create_player

# Verbose output
pytest -v

# Stop on first failure
pytest -x
```

---

### pytest-asyncio - Async Testing

**What it does:** Allows testing async functions

**Example:**
```python
import pytest

@pytest.mark.asyncio
async def test_async_function():
    result = await some_async_function()
    assert result == expected_value
```

**Why we need it:** FastAPI uses async functions, so we need to test them.

---

### pytest-cov - Coverage Reporter

**What it does:** Measures which lines of code are tested

**Usage:**
```powershell
# Run with coverage
pytest --cov=app

# Generate HTML report
pytest --cov=app --cov-report=html

# Open report
start htmlcov/index.html
```

**Coverage goals:**
- 🟢 80%+ = Excellent
- 🟡 60-80% = Good
- 🔴 <60% = Needs improvement

**What to cover:**
- ✅ All business logic
- ✅ All API endpoints
- ✅ Error handling paths
- ❌ Don't obsess over 100% (diminishing returns)

---

### httpx - HTTP Client

**What it does:** Makes HTTP requests in tests (via TestClient)

**Example:**
```python
from fastapi.testclient import TestClient

client = TestClient(app)
response = client.get("/api/v1/players/")
assert response.status_code == 200
```

**Why we need it:** To test FastAPI endpoints without running a server.

---

### Fixtures - Test Setup

**What they are:** Reusable test setup code

**Example:**
```python
import pytest

@pytest.fixture
def sample_player():
    """Create a test player."""
    return Player(
        username="testuser",
        character_name="Test Hero"
    )

def test_player_creation(sample_player):
    """Use the fixture."""
    assert sample_player.username == "testuser"
```

**Fixture scopes:**
- `function` (default) - Run for each test
- `class` - Run once per test class
- `module` - Run once per test file
- `session` - Run once per test session

---

## Running Tests

### Quick Start

```powershell
# Run all tests
.\scripts\test.ps1

# Or manually
cd backend
pytest

# With coverage
pytest --cov=app --cov-report=html
```

---

### Test Commands Reference

| Command | What It Does |
|---------|-------------|
| `pytest` | Run all tests |
| `pytest -v` | Verbose output |
| `pytest -x` | Stop on first failure |
| `pytest -s` | Show print statements |
| `pytest --lf` | Run last failed tests |
| `pytest --ff` | Run failed tests first |
| `pytest -k "player"` | Run tests with "player" in name |
| `pytest --collect-only` | List all tests without running |
| `pytest --markers` | List available markers |

---

### Running Specific Tests

```powershell
# Run one file
pytest backend/tests/test_api.py

# Run one test
pytest backend/tests/test_api.py::test_create_player

# Run tests matching pattern
pytest -k "player"

# Run marked tests
pytest -m "slow"
```

---

### CI/CD Testing

Tests run automatically on every push via GitHub Actions:

```yaml
# .github/workflows/ci-cd.yml
jobs:
  test-backend:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.11", "3.12"]
    steps:
      - name: Run tests
        run: |
          pytest --cov=app --cov-report=xml
      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

**What happens:**
1. ✅ Code pushed to GitHub
2. ✅ Tests run on Python 3.11 and 3.12
3. ✅ Coverage report uploaded
4. ✅ Pull request blocked if tests fail

---

## Writing Tests

### Test Structure

**Follow AAA pattern:**
- **Arrange** - Set up test data
- **Act** - Execute the code being tested
- **Assert** - Verify the results

```python
def test_player_health_increase():
    # Arrange
    player = Player(health=50, max_health=100)
    potion = Item(name="Health Potion", healing=30)
    
    # Act
    player.use_item(potion)
    
    # Assert
    assert player.health == 80
```

---

### Example 1: Testing a Model

```python
"""Test models (Unit Test)."""

def test_player_creation():
    """Test creating a player."""
    player = Player(
        username="testuser",
        character_name="Test Hero"
    )
    
    assert player.username == "testuser"
    assert player.character_name == "Test Hero"


def test_player_unique_username(db_session):
    """Test that usernames must be unique."""
    # Create first player
    player1 = Player(username="testuser", character_name="Hero 1")
    db_session.add(player1)
    db_session.commit()
    
    # Try to create second player with same username
    player2 = Player(username="testuser", character_name="Hero 2")
    db_session.add(player2)
    
    with pytest.raises(IntegrityError):
        db_session.commit()
```

---

### Example 2: Testing an API Endpoint

```python
"""Test API endpoints (Integration Test)."""

def test_create_player(client):
    """Test POST /api/v1/players/."""
    response = client.post(
        "/api/v1/players/",
        json={
            "username": "testuser",
            "character_name": "Test Hero"
        }
    )
    
    # Check status code
    assert response.status_code == 201
    
    # Check response data
    data = response.json()
    assert data["username"] == "testuser"
    assert data["character_name"] == "Test Hero"
    assert "id" in data
    assert "created_at" in data


def test_create_player_duplicate_username(client, db_session):
    """Test that duplicate usernames are rejected."""
    # Create first player
    client.post(
        "/api/v1/players/",
        json={"username": "testuser", "character_name": "Hero 1"}
    )
    
    # Try to create second player with same username
    response = client.post(
        "/api/v1/players/",
        json={"username": "testuser", "character_name": "Hero 2"}
    )
    
    assert response.status_code == 400
    assert "already exists" in response.json()["detail"].lower()
```

---

### Example 3: Testing Game Logic

```python
"""Test game engine (Unit Test)."""

def test_move_command(client, db_session):
    """Test moving between locations."""
    # Setup: Create player and game state
    player = create_test_player(db_session)
    
    # Act: Move north
    response = client.post(
        "/api/v1/game/command",
        json={
            "player_id": player.id,
            "command": "GO NORTH"
        }
    )
    
    # Assert: Check new location
    data = response.json()
    assert data["success"] is True
    assert "traveled north" in data["message"].lower()
    assert data["location"]["name"] == "Dark Forest"


def test_attack_enemy(client, db_session):
    """Test combat system."""
    # Setup
    player = create_test_player(db_session)
    spawn_enemy(db_session, player.game_state.current_location_id, "Goblin")
    
    # Act
    response = client.post(
        "/api/v1/game/command",
        json={
            "player_id": player.id,
            "command": "ATTACK GOBLIN"
        }
    )
    
    # Assert
    data = response.json()
    assert data["success"] is True
    assert "attack" in data["message"].lower()
```

---

### Parametrized Tests

Test the same logic with different inputs:

```python
@pytest.mark.parametrize("command,expected_direction", [
    ("GO NORTH", "north"),
    ("GO SOUTH", "south"),
    ("GO EAST", "east"),
    ("GO WEST", "west"),
])
def test_movement_commands(client, db_session, command, expected_direction):
    """Test all movement commands."""
    player = create_test_player(db_session)
    
    response = client.post(
        "/api/v1/game/command",
        json={"player_id": player.id, "command": command}
    )
    
    assert expected_direction in response.json()["message"].lower()
```

**Benefit:** One test function, multiple test cases.

---

### Testing Error Cases

**Always test error paths!**

```python
def test_invalid_command(client, db_session):
    """Test that invalid commands are handled."""
    player = create_test_player(db_session)
    
    response = client.post(
        "/api/v1/game/command",
        json={
            "player_id": player.id,
            "command": "INVALID COMMAND"
        }
    )
    
    assert response.status_code == 400
    assert "not recognized" in response.json()["message"].lower()


def test_player_not_found(client):
    """Test error when player doesn't exist."""
    response = client.post(
        "/api/v1/game/command",
        json={
            "player_id": 99999,
            "command": "LOOK"
        }
    )
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

---

## Test Organization

### File Structure

```
backend/tests/
├── __init__.py
├── conftest.py           # Fixtures and configuration
├── test_api.py           # API endpoint tests
├── test_game_engine.py   # Game logic tests
└── test_models.py        # Database model tests (future)
```

---

### conftest.py - Shared Fixtures

**Location:** `backend/tests/conftest.py`

**Purpose:** Define reusable fixtures for all tests

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.core.database import Base, get_db

# Test database (in-memory SQLite)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


@pytest.fixture(scope="function")
def db_session():
    """
    Create a fresh database for each test.
    
    Ensures test isolation - each test gets a clean database.
    """
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client with test database.
    
    Overrides the normal database dependency with our test database.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
```

**Key concepts:**
- `scope="function"` - Fresh fixture for each test
- `yield` - Provides fixture, then cleans up
- `dependency_overrides` - Swap real DB with test DB

---

### Test Naming

**Convention:** `test_<what>_<condition>_<expected>`

✅ Good names:
- `test_create_player_valid_data_returns_201`
- `test_create_player_duplicate_username_returns_400`
- `test_move_north_valid_location_updates_position`

❌ Bad names:
- `test_1`
- `test_player`
- `test_stuff`

---

### Test Documentation

```python
def test_create_player_with_duplicate_username(client, db_session):
    """
    Test that creating a player with duplicate username fails.
    
    Given: An existing player with username "testuser"
    When: Attempting to create another player with username "testuser"
    Then: Should return 400 status code with appropriate error message
    """
    # Test implementation...
```

---

## Test Coverage

### What is Coverage?

**Coverage** = Percentage of code executed by tests

```python
def calculate_damage(weapon, armor):
    base_damage = weapon.damage
    if armor:                        # ← Line 3
        return base_damage - armor   # ← Line 4 (covered)
    return base_damage               # ← Line 5 (not covered!)
```

If your test only tests with armor, line 5 is **not covered**.

---

### Viewing Coverage

```powershell
# Generate coverage report
pytest --cov=app --cov-report=html

# Open in browser
start htmlcov/index.html
```

**Coverage report shows:**
- 📊 Overall percentage
- 📄 Per-file percentage
- 🔴 Lines not covered (highlighted in red)
- 🟢 Lines covered (highlighted in green)

---

### Coverage Goals

| Coverage | Status | Action |
|----------|--------|--------|
| 90%+ | 🏆 Excellent | Maintain |
| 80-90% | ✅ Very Good | Minor improvements |
| 70-80% | 🟢 Good | Add tests for critical paths |
| 60-70% | 🟡 Acceptable | Prioritize important code |
| <60% | 🔴 Poor | Significant testing needed |

**Don't chase 100%:**
- Some code is hard to test (UI, external APIs)
- Diminishing returns after 80-90%
- Focus on critical business logic

---

### What to Prioritize

**High priority** (must test):
- ✅ Business logic (game engine, combat, inventory)
- ✅ Data validation (Pydantic schemas)
- ✅ API endpoints
- ✅ Database operations
- ✅ Error handling

**Medium priority**:
- ✅ Utility functions
- ✅ Configuration loading
- ✅ Data transformations

**Low priority**:
- ❌ Simple getters/setters
- ❌ Framework boilerplate
- ❌ Third-party library code

---

## Best Practices

### 1. Test Isolation

**Each test should be independent.**

❌ Bad:
```python
# Tests depend on each other
def test_1_create_player():
    global player_id
    player_id = create_player()

def test_2_update_player():
    update_player(player_id)  # Depends on test_1!
```

✅ Good:
```python
def test_create_player(db_session):
    player = create_player(db_session)
    assert player.id is not None

def test_update_player(db_session):
    player = create_player(db_session)  # Each test sets up its own data
    player.username = "updated"
    assert player.username == "updated"
```

---

### 2. Test One Thing

**Each test should verify one behavior.**

❌ Bad:
```python
def test_everything(client):
    # Create player
    response = client.post(...)
    assert response.status_code == 201
    
    # Update player
    response = client.put(...)
    assert response.status_code == 200
    
    # Delete player
    response = client.delete(...)
    assert response.status_code == 204
    
    # Too much in one test!
```

✅ Good:
```python
def test_create_player(client):
    response = client.post(...)
    assert response.status_code == 201

def test_update_player(client):
    # Setup...
    response = client.put(...)
    assert response.status_code == 200

def test_delete_player(client):
    # Setup...
    response = client.delete(...)
    assert response.status_code == 204
```

---

### 3. Descriptive Assertions

❌ Bad:
```python
assert response.status_code == 200
```

✅ Good:
```python
assert response.status_code == 200, f"Expected 200, got {response.status_code}. Response: {response.json()}"
```

Or use pytest's built-in feature:
```python
assert response.status_code == 200  # pytest shows values automatically
```

---

### 4. Use Fixtures for Setup

❌ Bad:
```python
def test_1():
    player = Player(username="test", character_name="Hero")
    # Test...

def test_2():
    player = Player(username="test", character_name="Hero")
    # Test...
```

✅ Good:
```python
@pytest.fixture
def sample_player():
    return Player(username="test", character_name="Hero")

def test_1(sample_player):
    # Use sample_player

def test_2(sample_player):
    # Use sample_player
```

---

### 5. Test Edge Cases

**Don't just test happy paths!**

```python
def test_inventory_add_item():
    """Test adding item to inventory."""
    # Happy path
    inventory = Inventory()
    inventory.add("Sword")
    assert "Sword" in inventory
    
    # Edge case: Duplicate items
    inventory.add("Sword")
    assert inventory.count("Sword") == 2
    
    # Edge case: Full inventory
    for i in range(100):
        inventory.add(f"Item{i}")
    
    with pytest.raises(InventoryFullError):
        inventory.add("One more item")
    
    # Edge case: Invalid item
    with pytest.raises(ValueError):
        inventory.add(None)
```

---

### 6. Keep Tests Fast

**Slow tests = Tests don't get run**

✅ Do:
- Use in-memory database (SQLite) for tests
- Mock external services
- Parallelize tests (`pytest -n auto`)

❌ Don't:
- Hit real databases
- Make real API calls
- Add unnecessary sleeps

---

### 7. Clean Test Data

```python
def test_with_cleanup(db_session):
    """Test always cleans up."""
    try:
        # Test code
        player = create_player(db_session)
        # Assertions...
    finally:
        # Cleanup (or use fixture with yield)
        db_session.query(Player).delete()
        db_session.commit()
```

**Or better: Use fixtures with `yield`**

---

## Common Patterns

### Pattern 1: Factory Functions

```python
def create_test_player(db_session, **kwargs):
    """Factory for creating test players."""
    defaults = {
        "username": f"testuser_{uuid.uuid4().hex[:8]}",
        "character_name": "Test Hero"
    }
    defaults.update(kwargs)
    
    player = Player(**defaults)
    db_session.add(player)
    db_session.commit()
    return player

# Usage
def test_something(db_session):
    player1 = create_test_player(db_session)
    player2 = create_test_player(db_session, username="custom")
```

---

### Pattern 2: Context Managers for Cleanup

```python
from contextlib import contextmanager

@contextmanager
def temporary_player(db_session):
    """Create player, automatically clean up."""
    player = create_player(db_session)
    try:
        yield player
    finally:
        db_session.delete(player)
        db_session.commit()

# Usage
def test_something(db_session):
    with temporary_player(db_session) as player:
        # Use player
        # Automatically deleted after block
```

---

### Pattern 3: Mocking External Services

```python
from unittest.mock import Mock, patch

def test_api_call():
    """Test code that calls external API."""
    with patch('requests.get') as mock_get:
        # Set up mock response
        mock_get.return_value.json.return_value = {"data": "test"}
        mock_get.return_value.status_code = 200
        
        # Call function that uses requests.get
        result = fetch_external_data()
        
        # Verify
        assert result == {"data": "test"}
        mock_get.assert_called_once()
```

---

## Troubleshooting

### Tests Failing Locally

**Problem:** Tests pass in CI but fail locally (or vice versa)

**Solutions:**
1. Check Python version: `python --version`
2. Check dependencies: `pip install -r requirements-dev.txt`
3. Delete test database: `del test.db`
4. Check database state: Tests may not be isolated

---

### Slow Tests

**Problem:** Test suite takes too long

**Solutions:**
1. Run in parallel: `pytest -n auto` (requires `pytest-xdist`)
2. Use SQLite instead of PostgreSQL for tests
3. Mock expensive operations
4. Mark slow tests: `@pytest.mark.slow`
5. Run fast tests first: `pytest -x --ff`

---

### Flaky Tests

**Problem:** Tests sometimes pass, sometimes fail

**Common causes:**
1. **Race conditions** - Async timing issues
2. **External dependencies** - Network, filesystem
3. **Test order dependency** - Tests affect each other
4. **Random data** - Use fixed seeds

**Solutions:**
```python
import random
random.seed(42)  # Fixed seed for reproducibility

# Or use pytest plugin
pytest --randomly-seed=42
```

---

### Import Errors

**Problem:** `ModuleNotFoundError` in tests

**Solution:**
```powershell
# Make sure you're in backend directory
cd backend

# Install in development mode
pip install -e .

# Or set PYTHONPATH
$env:PYTHONPATH = "."
pytest
```

---

### Database Locked (SQLite)

**Problem:** `OperationalError: database is locked`

**Solution:**
```python
# In conftest.py, ensure proper cleanup
@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()  # Important!
        Base.metadata.drop_all(bind=engine)
```

---

## Additional Resources

### Documentation
- **pytest docs**: https://docs.pytest.org/
- **FastAPI testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **SQLAlchemy testing**: https://docs.sqlalchemy.org/en/latest/orm/session_transaction.html

### Books
- "Test Driven Development: By Example" by Kent Beck
- "Python Testing with pytest" by Brian Okken

### Tools
- **pytest-xdist**: Run tests in parallel
- **pytest-watch**: Auto-run tests on file changes
- **pytest-mock**: Better mocking support
- **Hypothesis**: Property-based testing

---

## Summary

### Key Takeaways

1. ✅ **Write tests** - They save time in the long run
2. ✅ **Start simple** - Unit tests for functions, integration tests for APIs
3. ✅ **Test isolation** - Each test should be independent
4. ✅ **Test edge cases** - Not just happy paths
5. ✅ **Aim for 80% coverage** - But don't obsess over 100%
6. ✅ **Keep tests fast** - Or they won't get run
7. ✅ **Use fixtures** - DRY principle applies to tests too
8. ✅ **Run tests often** - Locally and in CI/CD

### Quick Reference Commands

```powershell
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test
pytest backend/tests/test_api.py::test_create_player

# Run in parallel
pytest -n auto

# Stop on first failure
pytest -x

# Show print statements
pytest -s
```

---

**Happy testing! May your tests always be green! 🟢**
