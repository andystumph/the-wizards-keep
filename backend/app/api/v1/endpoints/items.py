"""
Item API Endpoints

These endpoints provide information about game items.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Item, PlayerInventory
from app.schemas.schemas import InventoryItemResponse, ItemResponse

router = APIRouter()


@router.get("/", response_model=List[ItemResponse])
def list_items(
    item_type: str | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all items, optionally filtered by type.
    """
    query = db.query(Item)

    if item_type is not None:
        query = query.filter(Item.item_type == item_type)  # type: ignore[arg-type]

    items = query.offset(skip).limit(limit).all()
    return items


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(
    item_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific item by ID."""
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with ID {item_id} not found",
        )
    return item


@router.get("/player/{player_id}/inventory", response_model=List[InventoryItemResponse])
def get_player_inventory(
    player_id: int,
    db: Session = Depends(get_db),
):
    """Get all items in a player's inventory."""
    inventory = (
        db.query(PlayerInventory).filter(PlayerInventory.player_id == player_id).all()
    )
    return inventory
