# 3-Tier Architecture Guide

## Overview

The Wizard's Keep implements a **3-tier architecture**, one of the most common patterns in modern web applications. This architecture separates concerns into three distinct layers, each with its own responsibilities.

## The Three Tiers

```
┌─────────────────────────────────────────────────────────────┐
│                 PRESENTATION TIER (Tier 1)                  │
│                         Frontend                            │
│                  HTML + CSS + JavaScript                    │
│                                                             │
│  Responsibilities:                                          │
│  • Display game interface to user                           │
│  • Capture user input (commands)                            │
│  • Send HTTP requests to API                                │
│  • Render responses                                         │
└─────────────────────────────────────────────────────────────┘
                              ↓
                         HTTP/REST API
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                 APPLICATION TIER (Tier 2)                   │
│                        Backend API                          │
│                     FastAPI + Python                        │
│                                                             │
│  Responsibilities:                                          │
│  • Process game commands                                    │
│  • Implement business logic                                 │
│  • Validate input                                           │
│  • Coordinate between frontend and database                 │
│  • Enforce game rules                                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
                            SQL
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                      DATA TIER (Tier 3)                     │
│                         Database                            │
│                        PostgreSQL                           │
│                                                             │
│  Responsibilities:                                          │
│  • Store game world data                                    │
│  • Store player profiles and progress                       │
│  • Ensure data integrity                                    │
│  • Provide fast data access                                 │
└─────────────────────────────────────────────────────────────┘
```

## Benefits of 3-Tier Architecture

### 1. Separation of Concerns
Each tier has a specific purpose:
- **Frontend**: User interface and experience
- **Backend**: Business logic and data processing
- **Database**: Data persistence and integrity

### 2. Independent Scaling
Each tier can be scaled independently:
- Need more frontend capacity? Add more web servers
- Backend bottleneck? Add more API servers
- Database under load? Optimize queries or add read replicas

### 3. Technology Flexibility
Each tier can use the best technology for its purpose:
- **Frontend**: HTML/CSS/JS (could be React, Vue, Angular)
- **Backend**: Python with FastAPI (could be Node.js, Java, Go)
- **Database**: PostgreSQL (could be MySQL, MongoDB, etc.)

### 4. Enhanced Security
Security can be implemented at each layer:
- **Frontend**: Input validation, XSS prevention
- **Backend**: Authentication, authorization, business rule enforcement
- **Database**: Access control, encryption at rest

### 5. Easier Maintenance
Changes in one tier don't require changes in others (as long as the interface stays the same):
- Update UI without touching backend code
- Change business logic without modifying database schema
- Migrate to a new database without changing API

## Implementation in The Wizard's Keep

### Tier 1: Frontend
**Location**: `frontend/`

**Technology**: Vanilla JavaScript (no framework)

**Key Files**:
- `index.html`: Structure
- `css/style.css`: Styling
- `js/game.js`: Game logic
- `js/api.js`: API communication

**Communication**: Makes HTTP requests to Backend API at `http://localhost:8000/api/v1/`

### Tier 2: Backend API
**Location**: `backend/app/`

**Technology**: FastAPI (Python web framework)

**Key Components**:
- `main.py`: Application entry point
- `api/v1/endpoints/`: REST API endpoints
- `services/game_engine.py`: Business logic
- `models/models.py`: Database ORM models
- `schemas/schemas.py`: Data validation schemas

**Communication**: 
- Receives HTTP requests from Frontend
- Makes SQL queries to Database

### Tier 3: Database
**Technology**: PostgreSQL 15

**Key Tables**:
- `players`: User accounts
- `game_states`: Current game progress
- `locations`: Game world places
- `items`: Weapons, potions, etc.
- `enemies`: Monsters to fight
- `player_inventory`: Items owned by players

## Request Flow Example

Let's trace what happens when a player types "GO NORTH":

### 1. Frontend (Tier 1)
```javascript
// User types "GO NORTH" and presses Enter
// game.js captures the input
const command = "GO NORTH";

// api.js sends HTTP POST request
fetch('http://localhost:8000/api/v1/game/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        player_id: 1,
        command: "GO NORTH"
    })
});
```

### 2. Backend API (Tier 2)
```python
# main.py receives the request
# Routes it to game.py endpoint

@router.post("/command")
def process_command(command_request: GameCommandRequest, db: Session):
    # game_engine.py processes the command
    engine = GameEngine(db)
    result = engine.process_command(
        player_id=command_request.player_id,
        command=command_request.command
    )
    
    # Game engine:
    # 1. Parses "GO NORTH"
    # 2. Checks current location's north_id
    # 3. Validates movement is possible
    # 4. Updates player's location in database
    # 5. Returns new location info
```

### 3. Database (Tier 3)
```sql
-- Backend executes SQL queries

-- Get current game state
SELECT * FROM game_states WHERE player_id = 1;

-- Get current location
SELECT * FROM locations WHERE id = current_location_id;

-- Update player location
UPDATE game_states 
SET current_location_id = 2 
WHERE player_id = 1;

-- Get new location details
SELECT * FROM locations WHERE id = 2;
```

### 4. Response Back to Frontend
```javascript
// Frontend receives response
{
    "success": true,
    "message": "You travel north to Dark Cave...",
    "location": {
        "id": 2,
        "name": "Dark Cave",
        "description": "A spooky cave..."
    }
}

// game.js displays the message to user
displayMessage("You travel north to Dark Cave...");
```

## Design Patterns Used

### 1. MVC (Model-View-Controller)
- **Model**: Database models (`models.py`)
- **View**: Frontend templates (`index.html`)
- **Controller**: API endpoints (`api/v1/endpoints/`)

### 2. Repository Pattern
- Database access is abstracted through SQLAlchemy ORM
- Business logic doesn't write SQL directly

### 3. Dependency Injection
- FastAPI provides `db: Session = Depends(get_db)`
- Makes testing easier (can inject mock database)

### 4. DTO (Data Transfer Objects)
- Pydantic schemas validate and serialize data
- API requests/responses use schemas, not database models directly

## Testing the Architecture

Each tier can be tested independently:

### Frontend Testing
- Test UI interactions
- Mock API responses
- Verify correct API calls are made

### Backend Testing
```python
# Test API endpoints with mock database
def test_move_command(client, db_session):
    response = client.post("/api/v1/game/command", json={
        "player_id": 1,
        "command": "GO NORTH"
    })
    assert response.status_code == 200
```

### Database Testing
- Test schema design
- Test data integrity constraints
- Test query performance

## Evolution and Scalability

As your application grows, you can:

### Horizontal Scaling
- Run multiple frontend servers behind a load balancer
- Run multiple backend API servers
- Use database read replicas for queries

### Microservices
The 3-tier architecture can evolve into microservices:
- Player service (authentication, profiles)
- Game engine service (command processing)
- World service (locations, items, enemies)

### Caching
Add a cache layer between tiers:
- Redis between frontend and backend (session data)
- Redis between backend and database (frequently accessed data)

### Message Queues
For asynchronous operations:
- Backend puts long-running tasks in a queue
- Worker processes handle them
- Results sent back via WebSocket

## Common Pitfalls to Avoid

### ❌ Business Logic in Frontend
Don't validate game rules in JavaScript - it can be bypassed!
```javascript
// BAD: Frontend checks if move is valid
if (canGoNorth) {
    sendCommand("GO NORTH");
}
```

Always validate on backend:
```python
# GOOD: Backend enforces rules
if not current_location.north_id:
    return error("Cannot go north")
```

### ❌ Direct Database Access from Frontend
Never connect frontend directly to database!
```javascript
// BAD: Frontend queries database
const db = connectToDatabase();
const player = db.query("SELECT * FROM players...");
```

Always go through API:
```javascript
// GOOD: Frontend calls API
const response = await fetch("/api/v1/players/1");
```

### ❌ Mixing Concerns
Keep each tier focused:
- Frontend shouldn't contain business logic
- Backend shouldn't generate HTML
- Database shouldn't enforce business rules (beyond basic constraints)

## Conclusion

The 3-tier architecture provides a solid foundation for web applications. It's:
- **Scalable**: Each tier scales independently
- **Maintainable**: Changes are isolated
- **Testable**: Each tier can be tested separately
- **Secure**: Multiple layers of security
- **Flexible**: Technologies can be swapped

Understanding this pattern is essential for modern web development!
