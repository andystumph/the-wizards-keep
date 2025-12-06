"""
Location API Endpoints

These endpoints provide information about game locations.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Location
from app.schemas.schemas import LocationResponse

router = APIRouter()


@router.get("/", response_model=List[LocationResponse])
def list_locations(
    level: int | None = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all locations, optionally filtered by level.
    """
    query = db.query(Location)

    if level is not None:
        query = query.filter(Location.level == level)

    locations = query.offset(skip).limit(limit).all()
    return locations


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific location by ID."""
    location = db.query(Location).filter(Location.id == location_id).first()
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found",
        )
    return location
