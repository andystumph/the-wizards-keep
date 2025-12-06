# API Reference

Complete documentation for The Wizard's Keep REST API.

**Base URL**: `http://localhost:8000/api/v1`

**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

## Authentication

Currently, no authentication is required (this is a learning project). In production, you would implement:
- JWT tokens
- OAuth2
- API keys

## Response Format

All endpoints return JSON.

Success response:
```json
{
  "data": { ... },
  "success": true
}
```

Error response:
```json
{
  "detail": "Error message here",
  "success": false
}
```

## Endpoints

### Health Check

#### `GET /health`
Check if the API is running.

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "database": "connected"
}
```

---

## Players

### Create Player

#### `POST /api/v1/players/`
Create a new player account.

**Request Body**:
```json
{
  "username": "thornwind",
  "character_name": "Kael Thornwind"
}
```

**Response** (201 Created):
```json
{
  "id": 1,
  "username": "thornwind",
  "character_name": "Kael Thornwind",
  "created_at": "2025-12-02T10:30:00Z",
  "last_played": "2025-12-02T10:30:00Z"
}
```

**Errors**:
- `400`: Username already exists
- `422`: Validation error (missing fields, invalid format)

---

### Get Player

#### `GET /api/v1/players/{player_id}`
Retrieve player information.

**Parameters**:
- `player_id` (path, required): Player's ID

**Response** (200 OK):
```json
{
  "id": 1,
  "username": "thornwind",
  "character_name": "Kael Thornwind",
  "created_at": "2025-12-02T10:30:00Z",
  "last_played": "2025-12-02T10:45:00Z"
}
```

**Errors**:
- `404`: Player not found

---

### List Players

#### `GET /api/v1/players/`
List all players (with pagination).

**Query Parameters**:
- `skip` (optional, default: 0): Number of records to skip
- `limit` (optional, default: 100): Maximum records to return

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "username": "thornwind",
    "character_name": "Kael Thornwind",
    "created_at": "2025-12-02T10:30:00Z",
    "last_played": "2025-12-02T10:45:00Z"
  },
  ...
]
```

---

### Get Game State

#### `GET /api/v1/players/{player_id}/game-state`
Get the current game state for a player.

**Response** (200 OK):
```json
{
  "id": 1,
  "player_id": 1,
  "current_location_id": 5,
  "health": 85,
  "max_health": 100,
  "current_level": 1,
  "enemies_defeated": 3,
  "bosses_defeated": 0,
  "is_completed": false,
  "created_at": "2025-12-02T10:30:00Z",
  "updated_at": "2025-12-02T11:15:00Z"
}
```

**Errors**:
- `404`: Game state not found

---

### Delete Player

#### `DELETE /api/v1/players/{player_id}`
Delete a player and all associated data.

**Response** (204 No Content): Empty response

**Errors**:
- `404`: Player not found

---

## Game Commands

### Process Command

#### `POST /api/v1/game/command`
Send a game command and get the result.

**Request Body**:
```json
{
  "player_id": 1,
  "command": "GO NORTH"
}
```

**Response** (200 OK):
```json
{
  "success": true,
  "message": "You travel north to Dark Cave.\n\nA damp cave entrance...",
  "game_state": {
    "id": 1,
    "player_id": 1,
    "current_location_id": 3,
    "health": 85,
    "max_health": 100,
    "current_level": 1,
    "enemies_defeated": 3,
    "bosses_defeated": 0,
    "is_completed": false,
    "created_at": "2025-12-02T10:30:00Z",
    "updated_at": "2025-12-02T11:20:00Z"
  },
  "location": {
    "id": 3,
    "name": "Dark Cave",
    "description": "A damp cave entrance...",
    "location_type": "cave",
    "level": 1,
    "north_id": null,
    "south_id": 2,
    "east_id": null,
    "west_id": null,
    "up_id": null,
    "down_id": 5
  },
  "items": [
    {
      "id": 3,
      "name": "Rusty Sword",
      "description": "An old sword...",
      "item_type": "weapon",
      "damage": 5,
      "defense": 0,
      "healing": 0,
      "magic_power": 0,
      "is_takeable": true,
      "is_unique": false,
      "required_for_boss": false
    }
  ],
  "enemies": []
}
```

**Available Commands**:

**Movement**:
- `GO NORTH`, `GO SOUTH`, `GO EAST`, `GO WEST`, `GO UP`, `GO DOWN`

**Observation**:
- `LOOK` - Look around current location
- `EXAMINE [item]` - Examine an item
- `INVENTORY` - Check your inventory

**Interaction**:
- `TAKE [item]` - Pick up an item
- `DROP [item]` - Drop an item
- `USE [item]` - Use a consumable item
- `EQUIP [item]` - Equip weapon or armor

**Combat**:
- `ATTACK [enemy]` - Attack an enemy
- `FLEE` - Attempt to escape from combat

**System**:
- `STATS` - Show character statistics
- `HELP` - Show available commands

**Errors**:
- `400`: Invalid command or player state
- `404`: Player not found

---

### Reset Game

#### `POST /api/v1/game/reset/{player_id}`
Reset a player's game to the beginning.

**Response** (200 OK):
```json
{
  "message": "Game reset successfully"
}
```

---

### Get Help

#### `GET /api/v1/game/help`
Get list of available commands.

**Response** (200 OK):
```json
{
  "commands": {
    "movement": [
      {
        "command": "GO NORTH",
        "description": "Move north"
      },
      ...
    ],
    "observation": [...],
    "interaction": [...],
    "combat": [...],
    "system": [...]
  }
}
```

---

## Locations

### List Locations

#### `GET /api/v1/locations/`
List all game locations.

**Query Parameters**:
- `level` (optional): Filter by level (1, 2, or 3)
- `skip` (optional, default: 0)
- `limit` (optional, default: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Forest Path",
    "description": "You stand at the edge...",
    "location_type": "forest",
    "level": 1,
    "north_id": 2,
    "south_id": null,
    "east_id": null,
    "west_id": null,
    "up_id": null,
    "down_id": null
  },
  ...
]
```

---

### Get Location

#### `GET /api/v1/locations/{location_id}`
Get details of a specific location.

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Forest Path",
  "description": "You stand at the edge...",
  "location_type": "forest",
  "level": 1,
  "north_id": 2,
  "south_id": null,
  "east_id": null,
  "west_id": null,
  "up_id": null,
  "down_id": null
}
```

**Errors**:
- `404`: Location not found

---

## Items

### List Items

#### `GET /api/v1/items/`
List all items in the game.

**Query Parameters**:
- `item_type` (optional): Filter by type (weapon, armor, magic, consumable, key, treasure, quest)
- `skip` (optional, default: 0)
- `limit` (optional, default: 100)

**Response** (200 OK):
```json
[
  {
    "id": 1,
    "name": "Rusty Sword",
    "description": "An old sword...",
    "item_type": "weapon",
    "damage": 5,
    "defense": 0,
    "healing": 0,
    "magic_power": 0,
    "is_takeable": true,
    "is_unique": false,
    "required_for_boss": false
  },
  ...
]
```

---

### Get Item

#### `GET /api/v1/items/{item_id}`
Get details of a specific item.

**Response** (200 OK):
```json
{
  "id": 1,
  "name": "Rusty Sword",
  "description": "An old sword...",
  "item_type": "weapon",
  "damage": 5,
  "defense": 0,
  "healing": 0,
  "magic_power": 0,
  "is_takeable": true,
  "is_unique": false,
  "required_for_boss": false
}
```

**Errors**:
- `404`: Item not found

---

### Get Player Inventory

#### `GET /api/v1/items/player/{player_id}/inventory`
Get all items in a player's inventory.

**Response** (200 OK):
```json
[
  {
    "item": {
      "id": 1,
      "name": "Rusty Sword",
      "description": "An old sword...",
      "item_type": "weapon",
      "damage": 5,
      "defense": 0,
      "healing": 0,
      "magic_power": 0,
      "is_takeable": true,
      "is_unique": false,
      "required_for_boss": false
    },
    "quantity": 1,
    "equipped": true,
    "acquired_at": "2025-12-02T10:35:00Z"
  },
  ...
]
```

---

## Error Codes

| Status Code | Meaning |
|-------------|---------|
| 200 | Success |
| 201 | Created |
| 204 | No Content (successful deletion) |
| 400 | Bad Request (invalid input) |
| 404 | Not Found |
| 422 | Unprocessable Entity (validation error) |
| 500 | Internal Server Error |

## Rate Limiting

Currently no rate limiting is implemented (learning project).

In production, you would implement rate limiting to prevent abuse:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1638446400
```

## CORS

The API allows requests from:
- `http://localhost:8080` (frontend)
- `http://localhost:3000` (alternative port)

Configured in `backend/app/core/config.py`.

## Versioning

Current version: `v1` (in URL path `/api/v1/`)

When breaking changes are needed, create `v2`:
- `/api/v1/` - Old version (still supported)
- `/api/v2/` - New version (new features)

## Testing the API

### Using cURL
```powershell
# Create player
curl -X POST http://localhost:8000/api/v1/players/ `
  -H "Content-Type: application/json" `
  -d '{"username":"testuser","character_name":"Test Hero"}'

# Send command
curl -X POST http://localhost:8000/api/v1/game/command `
  -H "Content-Type: application/json" `
  -d '{"player_id":1,"command":"LOOK"}'
```

### Using Python
```python
import requests

# Create player
response = requests.post(
    "http://localhost:8000/api/v1/players/",
    json={"username": "testuser", "character_name": "Test Hero"}
)
player = response.json()

# Send command
response = requests.post(
    "http://localhost:8000/api/v1/game/command",
    json={"player_id": player["id"], "command": "LOOK"}
)
result = response.json()
print(result["message"])
```

### Using JavaScript
```javascript
// Create player
const response = await fetch('http://localhost:8000/api/v1/players/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'testuser',
        character_name: 'Test Hero'
    })
});
const player = await response.json();

// Send command
const cmdResponse = await fetch('http://localhost:8000/api/v1/game/command', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        player_id: player.id,
        command: 'LOOK'
    })
});
const result = await cmdResponse.json();
console.log(result.message);
```

## Interactive Documentation

FastAPI provides interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

You can test all endpoints directly from the browser!
