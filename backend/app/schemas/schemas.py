"""
Pydantic Schemas

Schemas define the shape of data for API requests and responses.
They provide validation, serialization, and documentation.

Educational Notes:
- Pydantic automatically validates incoming data
- Schemas are separate from database models (separation of concerns)
- BaseModel for input, orm_mode for output from database
- Type hints enable IDE autocomplete and catch bugs early
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

# ============================================================================
# Player Schemas
# ============================================================================


class PlayerBase(BaseModel):
    """Base schema with common player fields."""

    username: str = Field(
        ..., min_length=3, max_length=50, description="Unique username"
    )
    character_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Character's name in the game",
    )


class PlayerCreate(PlayerBase):
    """Schema for creating a new player."""

    pass


class PlayerResponse(PlayerBase):
    """Schema for player data in API responses."""

    id: int
    created_at: datetime
    last_played: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Location Schemas
# ============================================================================


class LocationBase(BaseModel):
    """Base location schema."""

    name: str
    description: str
    location_type: str
    level: int


class LocationResponse(LocationBase):
    """Schema for location data in responses."""

    id: int
    north_id: Optional[int] = None
    south_id: Optional[int] = None
    east_id: Optional[int] = None
    west_id: Optional[int] = None
    up_id: Optional[int] = None
    down_id: Optional[int] = None
    is_locked: bool = False
    required_key_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Item Schemas
# ============================================================================


class ItemBase(BaseModel):
    """Base item schema."""

    name: str
    description: str
    item_type: str


class ItemResponse(ItemBase):
    """Schema for item data in responses."""

    id: int
    damage: int = 0
    defense: int = 0
    healing: int = 0
    magic_power: int = 0
    is_takeable: bool = True
    is_unique: bool = False
    required_for_boss: bool = False

    model_config = ConfigDict(from_attributes=True)


class InventoryItemResponse(BaseModel):
    """Schema for items in player inventory."""

    item: ItemResponse
    quantity: int
    equipped: bool
    acquired_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Enemy Schemas
# ============================================================================


class EnemyBase(BaseModel):
    """Base enemy schema."""

    name: str
    description: str
    enemy_type: str


class EnemyResponse(EnemyBase):
    """Schema for enemy data in responses."""

    id: int
    health: int
    damage: int
    defense: int = 0
    is_boss: bool = False
    is_alive: bool = True
    level: int

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Game State Schemas
# ============================================================================


class GameStateResponse(BaseModel):
    """Schema for game state in responses."""

    id: int
    player_id: int
    current_location_id: int
    health: int
    max_health: int
    current_level: int
    enemies_defeated: int
    bosses_defeated: int
    is_completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# Game Command Schemas
# ============================================================================


class GameCommandRequest(BaseModel):
    """Schema for player commands."""

    command: str = Field(
        ..., min_length=1, max_length=200, description="Player's text command"
    )
    player_id: int = Field(..., description="ID of the player issuing the command")


class GameCommandResponse(BaseModel):
    """Schema for command results."""

    success: bool
    message: str
    game_state: Optional[GameStateResponse] = None
    location: Optional[LocationResponse] = None
    items: Optional[List[ItemResponse]] = None
    enemies: Optional[List[EnemyResponse]] = None
    inventory: Optional[List[InventoryItemResponse]] = None


# ============================================================================
# Combat Schemas
# ============================================================================


class CombatAction(BaseModel):
    """Schema for combat actions."""

    player_id: int
    enemy_id: int
    action: str = Field(..., pattern="^(attack|flee)$")


class CombatResult(BaseModel):
    """Schema for combat results."""

    success: bool
    message: str
    player_health: int
    enemy_health: int
    enemy_defeated: bool = False
    player_defeated: bool = False
    items_dropped: Optional[List[ItemResponse]] = None


# ============================================================================
# Helper Schemas
# ============================================================================


class MessageResponse(BaseModel):
    """Simple message response."""

    message: str


class HealthCheckResponse(BaseModel):
    """Health check response."""

    status: str
    version: str
    database: str
