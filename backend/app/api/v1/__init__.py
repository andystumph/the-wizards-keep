"""API version 1 routes."""

from fastapi import APIRouter

from app.api.v1.endpoints import game, items, locations, players

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(players.router, prefix="/players", tags=["Players"])
api_router.include_router(game.router, prefix="/game", tags=["Game"])
api_router.include_router(locations.router, prefix="/locations", tags=["Locations"])
api_router.include_router(items.router, prefix="/items", tags=["Items"])
