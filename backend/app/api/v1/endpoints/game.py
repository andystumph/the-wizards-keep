"""
Game API Endpoints

These endpoints handle the main game loop - processing player commands
and returning game state updates.

Educational Notes:
- This is the "controller" in MVC architecture
- Commands are parsed and delegated to service layer
- Stateless design: each request is independent
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.schemas import GameCommandRequest, GameCommandResponse
from app.services.game_engine import GameEngine

router = APIRouter()


@router.post("/command", response_model=GameCommandResponse)
def process_command(
    command_request: GameCommandRequest,
    db: Session = Depends(get_db),
):
    """
    Process a player command and return the result.

    This is the main endpoint for gameplay. Players send text commands
    like "GO NORTH" or "TAKE SWORD" and receive game state updates.

    Educational Note:
    The game engine handles all the business logic, keeping this
    endpoint thin and focused on HTTP concerns.
    """
    try:
        game_engine = GameEngine(db)
        result = game_engine.process_command(
            player_id=command_request.player_id,
            command=command_request.command,
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing command: {str(e)}",
        )


@router.post("/reset/{player_id}")
def reset_game(
    player_id: int,
    db: Session = Depends(get_db),
):
    """
    Reset a player's game to the beginning.

    This deletes their current game state and creates a fresh one.
    """
    game_engine = GameEngine(db)
    game_engine.reset_player_game(player_id)
    return {"message": "Game reset successfully"}


@router.get("/help")
def get_help():
    """
    Return available commands and their descriptions.

    Educational Note:
    Self-documenting APIs improve user experience. This endpoint
    provides in-game help without hardcoding it in the frontend.
    """
    return {
        "commands": {
            "movement": [
                {"command": "GO NORTH", "description": "Move north"},
                {"command": "GO SOUTH", "description": "Move south"},
                {"command": "GO EAST", "description": "Move east"},
                {"command": "GO WEST", "description": "Move west"},
                {"command": "GO UP", "description": "Move up (stairs, ladder, etc.)"},
                {"command": "GO DOWN", "description": "Move down"},
            ],
            "observation": [
                {"command": "LOOK", "description": "Look around the current location"},
                {"command": "EXAMINE [item]", "description": "Examine an item closely"},
                {"command": "INVENTORY", "description": "Check your inventory"},
            ],
            "interaction": [
                {"command": "TAKE [item]", "description": "Pick up an item"},
                {
                    "command": "DROP [item]",
                    "description": "Drop an item from inventory",
                },
                {"command": "USE [item]", "description": "Use an item"},
                {"command": "EQUIP [item]", "description": "Equip a weapon or armor"},
            ],
            "combat": [
                {"command": "ATTACK [enemy]", "description": "Attack an enemy"},
                {"command": "FLEE", "description": "Attempt to flee from combat"},
            ],
            "system": [
                {"command": "HELP", "description": "Show this help message"},
                {"command": "STATS", "description": "Show your character stats"},
                {"command": "QUIT", "description": "Save and quit the game"},
            ],
        }
    }
