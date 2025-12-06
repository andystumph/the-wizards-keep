"""
Database Models

These models represent the database schema using SQLAlchemy ORM.
Each class maps to a table in PostgreSQL.

Educational Notes:
- Models define the structure of your data
- Relationships define how tables connect to each other
- Indexes improve query performance on frequently searched columns
- Timestamps track when records are created/modified
"""

import enum
from datetime import datetime

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class Player(Base):
    """
    Player model stores user account and character information.

    Educational Note:
    This represents the "user" in our application. In a real game,
    you might separate "Account" and "Character" into different tables.
    """

    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    character_name = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_played = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    game_states = relationship(
        "GameState", back_populates="player", cascade="all, delete-orphan"
    )
    inventory_items = relationship(
        "PlayerInventory", back_populates="player", cascade="all, delete-orphan"
    )


class LocationType(str, enum.Enum):
    """Types of locations in the game."""

    FOREST = "forest"
    CAVE = "cave"
    DUNGEON = "dungeon"
    ROOM = "room"
    CORRIDOR = "corridor"
    TOWER = "tower"
    COURTYARD = "courtyard"


class Location(Base):
    """
    Location model defines places in the game world.

    Educational Note:
    Locations form a graph structure where each location can connect
    to others via directions (north, south, east, west, up, down).
    """

    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    location_type: LocationType = Column(Enum(LocationType), nullable=False)  # type: ignore
    level = Column(Integer, nullable=False, index=True)  # 1, 2, or 3

    # Connections to other locations (nullable if no exit in that direction)
    north_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    south_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    east_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    west_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    up_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    down_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # Locked door support
    is_locked = Column(Boolean, default=False)
    required_key_id = Column(Integer, ForeignKey("items.id"), nullable=True)

    # Relationships
    items = relationship(
        "Item", back_populates="location", foreign_keys="Item.location_id"
    )
    enemies = relationship("Enemy", back_populates="location")
    game_states = relationship("GameState", back_populates="current_location")


class ItemType(str, enum.Enum):
    """Types of items in the game."""

    WEAPON = "weapon"
    ARMOR = "armor"
    MAGIC = "magic"
    CONSUMABLE = "consumable"
    KEY = "key"
    TREASURE = "treasure"
    QUEST = "quest"


class Item(Base):
    """
    Item model defines objects that can be found and used in the game.

    Educational Note:
    Items can exist in locations or in player inventories.
    Some items are unique (like quest items), others can have multiple instances.
    """

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    item_type: ItemType = Column(Enum(ItemType), nullable=False)  # type: ignore

    # Item properties
    damage = Column(Integer, default=0)  # For weapons
    defense = Column(Integer, default=0)  # For armor
    healing = Column(Integer, default=0)  # For consumables
    magic_power = Column(Integer, default=0)  # For magic items

    # Flags
    is_takeable = Column(Boolean, default=True)
    is_unique = Column(Boolean, default=False)
    required_for_boss = Column(Boolean, default=False)

    # Location (null if in player inventory)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)
    # Original location for respawning items when game resets
    original_location_id = Column(Integer, ForeignKey("locations.id"), nullable=True)

    # Relationships
    location = relationship(
        "Location", back_populates="items", foreign_keys=[location_id]
    )
    player_inventories = relationship("PlayerInventory", back_populates="item")


class EnemyType(str, enum.Enum):
    """Types of enemies in the game."""

    ORC = "orc"
    GOBLIN = "goblin"
    KOBOLD = "kobold"
    TROLL = "troll"
    GNOLL = "gnoll"
    HOBGOBLIN = "hobgoblin"
    WIZARD = "wizard"


class Enemy(Base):
    """
    Enemy model defines hostile creatures in the game.

    Educational Note:
    Enemies are associated with locations. When defeated, they drop items
    and the player gains experience. Boss enemies are tougher and required
    to progress to the next level.
    """

    __tablename__ = "enemies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    enemy_type: EnemyType = Column(Enum(EnemyType), nullable=False)  # type: ignore

    # Combat stats
    health = Column(Integer, nullable=False)
    damage = Column(Integer, nullable=False)
    defense = Column(Integer, default=0)

    # Flags
    is_boss = Column(Boolean, default=False)
    is_alive = Column(Boolean, default=True)
    respawns = Column(Boolean, default=False)

    # Location
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    level = Column(Integer, nullable=False)  # Which level is this enemy in

    # Relationships
    location = relationship("Location", back_populates="enemies")


class GameState(Base):
    """
    GameState tracks the current state of a player's game.

    Educational Note:
    This is the "save game" table. It stores where the player is,
    their stats, and progress. There's one active game state per player.
    """

    __tablename__ = "game_states"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False, unique=True)

    # Current status
    current_location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    health = Column(Integer, nullable=False, default=100)
    max_health = Column(Integer, nullable=False, default=100)

    # Progress tracking
    current_level = Column(Integer, nullable=False, default=1)
    enemies_defeated = Column(Integer, default=0)
    bosses_defeated = Column(Integer, default=0)

    # Game completion
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    player = relationship("Player", back_populates="game_states")
    current_location = relationship("Location", back_populates="game_states")


class PlayerInventory(Base):
    """
    PlayerInventory is a junction table linking players to items.

    Educational Note:
    This is a many-to-many relationship. A player can have many items,
    and items can be possessed by different players (in different games).
    The quantity field allows stacking of identical items.
    """

    __tablename__ = "player_inventory"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    quantity = Column(Integer, default=1, nullable=False)
    equipped = Column(Boolean, default=False)  # For weapons/armor
    acquired_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    player = relationship("Player", back_populates="inventory_items")
    item = relationship("Item", back_populates="player_inventories")

    # Indexes for faster queries
    __table_args__ = (Index("idx_player_item", "player_id", "item_id"),)
