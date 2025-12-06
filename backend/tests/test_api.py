"""
API Endpoint Tests

Educational Notes:
- Integration tests verify API endpoints work correctly
- Test both success and failure cases
- Check response status codes, data structure, and content
"""

from fastapi import status


class TestPlayerEndpoints:
    """Tests for player management endpoints."""

    def test_create_player(self, client):
        """Test creating a new player."""
        response = client.post(
            "/api/v1/players/",
            json={"username": "testuser", "character_name": "Test Hero"},
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["username"] == "testuser"
        assert data["character_name"] == "Test Hero"
        assert "id" in data
        assert "created_at" in data

    def test_create_duplicate_player(self, client):
        """Test creating a player with duplicate username fails."""
        # Create first player
        client.post(
            "/api/v1/players/",
            json={"username": "testuser", "character_name": "Test Hero"},
        )

        # Try to create duplicate
        response = client.post(
            "/api/v1/players/",
            json={"username": "testuser", "character_name": "Another Hero"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already taken" in response.json()["detail"]

    def test_get_player(self, client):
        """Test retrieving a player by ID."""
        # Create player
        create_response = client.post(
            "/api/v1/players/",
            json={"username": "testuser", "character_name": "Test Hero"},
        )
        player_id = create_response.json()["id"]

        # Get player
        response = client.get(f"/api/v1/players/{player_id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == player_id
        assert data["username"] == "testuser"

    def test_get_nonexistent_player(self, client):
        """Test getting a player that doesn't exist."""
        response = client.get("/api/v1/players/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_get_player_game_state(self, client):
        """Test retrieving a player's game state."""
        # Create player
        create_response = client.post(
            "/api/v1/players/",
            json={"username": "testuser", "character_name": "Test Hero"},
        )
        player_id = create_response.json()["id"]

        # Get game state
        response = client.get(f"/api/v1/players/{player_id}/game-state")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["player_id"] == player_id
        assert data["health"] == 100
        assert data["current_level"] == 1


class TestGameEndpoints:
    """Tests for game command endpoints."""

    def test_help_command(self, client):
        """Test the help command."""
        response = client.get("/api/v1/game/help")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "commands" in data
        assert "movement" in data["commands"]
        assert "combat" in data["commands"]

    def test_game_command(self, client, db_session):
        """Test sending a game command."""
        # Create player and location
        from app.models.models import GameState, Location, LocationType, Player

        location = Location(
            id=1,
            name="Test Location",
            description="A test location",
            location_type=LocationType.FOREST,
            level=1,
        )
        db_session.add(location)
        db_session.commit()

        player = Player(username="testuser", character_name="Test Hero")
        db_session.add(player)
        db_session.commit()

        game_state = GameState(
            player_id=player.id,
            current_location_id=1,
            health=100,
            max_health=100,
            current_level=1,
        )
        db_session.add(game_state)
        db_session.commit()

        # Send LOOK command
        response = client.post(
            "/api/v1/game/command", json={"player_id": player.id, "command": "LOOK"}
        )

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["success"] is True
        assert "message" in data


class TestHealthEndpoint:
    """Tests for health check endpoint."""

    def test_health_check(self, client):
        """Test the health check endpoint."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
