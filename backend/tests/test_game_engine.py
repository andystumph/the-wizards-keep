"""
Game Engine Tests

Educational Notes:
- Unit tests verify individual components work correctly
- Test edge cases and error conditions
- Mock external dependencies when needed
"""

import pytest

from app.models.models import (
    Enemy,
    EnemyType,
    GameState,
    Item,
    ItemType,
    Location,
    LocationType,
    Player,
)
from app.services.game_engine import GameEngine


class TestGameEngine:
    """Tests for the game engine."""

    @pytest.fixture
    def game_world(self, db_session):
        """Create a basic game world for testing."""
        # Create locations
        loc1 = Location(
            id=1,
            name="Starting Room",
            description="A simple room",
            location_type=LocationType.ROOM,
            level=1,
            north_id=2,
        )
        loc2 = Location(
            id=2,
            name="North Room",
            description="A northern room",
            location_type=LocationType.ROOM,
            level=1,
            south_id=1,
        )
        db_session.add_all([loc1, loc2])

        # Create item
        item = Item(
            name="Test Sword",
            description="A test weapon",
            item_type=ItemType.WEAPON,
            damage=10,
            location_id=1,
            is_takeable=True,
        )
        db_session.add(item)

        # Create enemy
        enemy = Enemy(
            name="Test Goblin",
            description="A test enemy",
            enemy_type=EnemyType.GOBLIN,
            health=20,
            damage=5,
            location_id=2,
            level=1,
        )
        db_session.add(enemy)

        # Create player
        player = Player(username="testplayer", character_name="Test Hero")
        db_session.add(player)
        db_session.commit()

        # Create game state
        game_state = GameState(
            player_id=player.id,
            current_location_id=1,
            health=100,
            max_health=100,
            current_level=1,
        )
        db_session.add(game_state)
        db_session.commit()

        return {
            "player": player,
            "game_state": game_state,
            "loc1": loc1,
            "loc2": loc2,
            "item": item,
            "enemy": enemy,
        }

    def test_look_command(self, db_session, game_world):
        """Test the LOOK command."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "LOOK")

        assert result.success is True
        assert "Starting Room" in result.message
        assert "Test Sword" in result.message

    def test_movement_command(self, db_session, game_world):
        """Test movement between locations."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "GO NORTH")

        assert result.success is True
        assert "North Room" in result.message

        # Verify player moved
        game_state = game_world["game_state"]
        db_session.refresh(game_state)
        assert game_state.current_location_id == 2

    def test_invalid_movement(self, db_session, game_world):
        """Test movement in invalid direction."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "GO EAST")

        assert result.success is False
        assert "cannot go" in result.message.lower()

    def test_take_item(self, db_session, game_world):
        """Test taking an item."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "TAKE SWORD")

        assert result.success is True
        assert "take" in result.message.lower()

        # Verify item in inventory
        from app.models.models import PlayerInventory

        inventory = (
            db_session.query(PlayerInventory)
            .filter(PlayerInventory.player_id == game_world["player"].id)
            .first()
        )
        assert inventory is not None
        assert inventory.item_id == game_world["item"].id

    def test_inventory_command(self, db_session, game_world):
        """Test checking inventory."""
        engine = GameEngine(db_session)

        # Take an item first
        engine.process_command(game_world["player"].id, "TAKE SWORD")

        # Check inventory
        result = engine.process_command(game_world["player"].id, "INVENTORY")

        assert result.success is True
        assert "Test Sword" in result.message

    def test_stats_command(self, db_session, game_world):
        """Test checking character stats."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "STATS")

        assert result.success is True
        assert "Test Hero" in result.message
        assert "100" in result.message  # Health

    def test_help_command(self, db_session, game_world):
        """Test help command."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "HELP")

        assert result.success is True
        assert "MOVEMENT" in result.message or "movement" in result.message.lower()

    def test_unknown_command(self, db_session, game_world):
        """Test handling of unknown command."""
        engine = GameEngine(db_session)
        result = engine.process_command(game_world["player"].id, "DANCE")

        assert result.success is False
        assert (
            "don't understand" in result.message.lower()
            or "help" in result.message.lower()
        )

    def test_attack_enemy(self, db_session, game_world):
        """Test attacking an enemy."""
        engine = GameEngine(db_session)

        # Move to enemy location
        engine.process_command(game_world["player"].id, "GO NORTH")

        # Attack enemy
        result = engine.process_command(game_world["player"].id, "ATTACK GOBLIN")

        assert result.success is True
        assert "attack" in result.message.lower()

        # Verify enemy health decreased
        enemy = game_world["enemy"]
        db_session.refresh(enemy)
        assert enemy.health < 20
