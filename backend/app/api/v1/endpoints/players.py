"""
Player API Endpoints

These endpoints handle player creation, retrieval, and management.

Educational Notes:
- RESTful design: Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Dependency injection: FastAPI automatically provides the database session
- Status codes: Use correct HTTP status codes (201 for created, 404 for not found)
- Error handling: Provide clear error messages
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.models import GameState, Player
from app.schemas.schemas import GameStateResponse, PlayerCreate, PlayerResponse

router = APIRouter()


@router.post("/", response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player(
    player_data: PlayerCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new player.

    This also initializes a new game state for the player at the starting location.
    """
    # Check if username already exists
    existing_player = (
        db.query(Player).filter(Player.username == player_data.username).first()
    )
    if existing_player:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username '{player_data.username}' is already taken",
        )

    # Create new player
    new_player = Player(
        username=player_data.username,
        character_name=player_data.character_name,
    )
    db.add(new_player)
    db.commit()
    db.refresh(new_player)

    # Initialize game state for new player
    game_state = GameState(
        player_id=new_player.id,
        current_location_id=settings.STARTING_LOCATION_ID,
        health=settings.STARTING_HEALTH,
        max_health=settings.STARTING_HEALTH,
        current_level=1,
    )
    db.add(game_state)
    db.commit()

    return new_player


@router.get("/", response_model=List[PlayerResponse])
def list_players(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all players.

    Supports pagination via skip and limit parameters.
    """
    players = db.query(Player).offset(skip).limit(limit).all()
    return players


@router.get("/{player_id}", response_model=PlayerResponse)
def get_player(
    player_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific player by ID."""
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )
    return player


@router.get("/{player_id}/game-state", response_model=GameStateResponse)
def get_player_game_state(
    player_id: int,
    db: Session = Depends(get_db),
):
    """Get the current game state for a player."""
    game_state = db.query(GameState).filter(GameState.player_id == player_id).first()
    if not game_state:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No game state found for player {player_id}",
        )
    return game_state


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(
    player_id: int,
    db: Session = Depends(get_db),
):
    """
    Delete a player and all associated data.

    Educational Note:
    This demonstrates cascade deletion - when a player is deleted,
    their game state and inventory are automatically deleted due to
    the cascade="all, delete-orphan" relationship configuration.
    """
    player = db.query(Player).filter(Player.id == player_id).first()
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with ID {player_id} not found",
        )

    db.delete(player)
    db.commit()
    return None
