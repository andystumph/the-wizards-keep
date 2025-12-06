"""
Game Engine

This module contains the core game logic - command parsing, state management,
and game mechanics.

Educational Notes:
- Separation of concerns: business logic is separate from API layer
- Single Responsibility: each method does one thing well
- Command pattern: commands are parsed and executed
- State management: game state is persisted to database
"""

import re
from datetime import datetime
from typing import Optional

from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.models import (
    Enemy,
    GameState,
    Item,
    ItemType,
    Location,
    PlayerInventory,
)
from app.schemas.schemas import GameCommandResponse


class GameEngine:
    """
    The game engine processes player commands and manages game state.

    This is the "brain" of the game that interprets commands and
    determines what happens next.
    """

    def __init__(self, db: Session):
        """Initialize the game engine with a database session."""
        self.db = db

        # Command patterns for parsing
        self.command_patterns = {
            "go": r"^go\s+(north|south|east|west|up|down)$",
            "look": r"^look(\s+around)?$",
            "examine": r"^examine\s+(.+)$",
            "take": r"^take\s+(.+)$",
            "drop": r"^drop\s+(.+)$",
            "use": r"^use\s+(.+)$",
            "equip": r"^equip\s+(.+)$",
            "attack": r"^attack\s+(.+)$",
            "flee": r"^flee$",
            "inventory": r"^inventory$",
            "stats": r"^stats$",
            "help": r"^help$",
        }

    def process_command(self, player_id: int, command: str) -> GameCommandResponse:
        """
        Process a player command and return the result.

        This is the main entry point for game actions.
        """
        # Normalize command (lowercase, strip whitespace)
        normalized_command = command.strip().lower()

        # Get player and game state
        game_state = self._get_game_state(player_id)
        if not game_state:
            return GameCommandResponse(
                success=False,
                message="Game state not found. Please create a new player.",
            )

        # Update last played timestamp
        game_state.player.last_played = datetime.utcnow()

        # Parse and execute command
        try:
            result = self._parse_and_execute(normalized_command, game_state)
            self.db.commit()
            return result
        except Exception as e:
            self.db.rollback()
            return GameCommandResponse(
                success=False,
                message=f"Error processing command: {str(e)}",
            )

    def _parse_and_execute(
        self, command: str, game_state: GameState
    ) -> GameCommandResponse:
        """Parse the command and execute the appropriate action."""

        # Try to match command against patterns
        for cmd_type, pattern in self.command_patterns.items():
            match = re.match(pattern, command)
            if match:
                # Call the appropriate handler method
                handler = getattr(self, f"_handle_{cmd_type}", None)
                if handler:
                    return handler(game_state, match)  # type: ignore[no-any-return]

        # Command not recognized
        return GameCommandResponse(
            success=False,
            message=f"I don't understand '{command}'. Type HELP for available commands.",
        )

    # ========================================================================
    # Command Handlers
    # ========================================================================

    def _handle_go(self, game_state: GameState, match: re.Match) -> GameCommandResponse:
        """Handle movement commands (GO NORTH, GO SOUTH, etc.)."""
        direction = match.group(1)
        current_location = game_state.current_location

        # Get the location ID for the specified direction
        direction_map = {
            "north": current_location.north_id,
            "south": current_location.south_id,
            "east": current_location.east_id,
            "west": current_location.west_id,
            "up": current_location.up_id,
            "down": current_location.down_id,
        }

        new_location_id = direction_map.get(direction)

        if not new_location_id:
            return GameCommandResponse(
                success=False,
                message=f"You cannot go {direction} from here.",
            )

        # Check if the destination location is locked
        destination_location = (
            self.db.query(Location).filter(Location.id == new_location_id).first()
        )

        if destination_location and destination_location.is_locked:
            # Check if player has the required key in their inventory
            if destination_location.required_key_id:
                has_key = (
                    self.db.query(PlayerInventory)
                    .filter(
                        PlayerInventory.player_id == game_state.player_id,
                        PlayerInventory.item_id == destination_location.required_key_id,
                    )
                    .first()
                )

                if not has_key:
                    # Get key name for the error message
                    required_key = (
                        self.db.query(Item)
                        .filter(Item.id == destination_location.required_key_id)
                        .first()
                    )
                    key_name = required_key.name if required_key else "a key"

                    return GameCommandResponse(
                        success=False,
                        message=f"The way {direction} is locked! You need {key_name} to proceed.",
                    )
                else:
                    # Player has the key - unlock the door permanently
                    destination_location.is_locked = False  # type: ignore[assignment]
                    self.db.commit()

                    return GameCommandResponse(
                        success=True,
                        message=f"You use the {has_key.item.name} to unlock the door {direction}. The way is now open!",
                    )

        # Check if there are hostile enemies blocking the way
        enemies = (
            self.db.query(Enemy)
            .filter(
                Enemy.location_id == current_location.id,
                Enemy.is_alive.is_(True),
            )
            .all()
        )

        if enemies:
            enemy_names = ", ".join([str(e.name) for e in enemies])
            message = (
                f"You cannot leave while {enemy_names} blocks your path! "
                "You must defeat them or FLEE."
            )
            return GameCommandResponse(
                success=False,
                message=message,
            )

        # Move to new location
        game_state.current_location_id = new_location_id
        new_location = (
            self.db.query(Location).filter(Location.id == new_location_id).first()
        )

        # Get items and enemies at new location
        items = self.db.query(Item).filter(Item.location_id == new_location_id).all()
        enemies = (
            self.db.query(Enemy)
            .filter(Enemy.location_id == new_location_id, Enemy.is_alive.is_(True))
            .all()
        )

        # Build description
        if new_location is None:
            return GameCommandResponse(
                success=False,
                message="Error: destination location not found.",
            )

        message = f"You travel {direction} to {new_location.name}.\n\n{new_location.description}"

        if items:
            item_names = ", ".join([str(item.name) for item in items])
            message += f"\n\nYou see: {item_names}"

        if enemies:
            enemy_names = ", ".join([str(enemy.name) for enemy in enemies])
            message += f"\n\n⚔️ Warning! You encounter: {enemy_names}"

        return GameCommandResponse(
            success=True,
            message=message,
            game_state=game_state,
            location=new_location,  # type: ignore[arg-type]
            items=items,  # type: ignore[arg-type]
            enemies=enemies,  # type: ignore[arg-type]
        )

    def _handle_look(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle LOOK command to describe current location."""
        location = game_state.current_location

        # Get items and enemies at location
        items = self.db.query(Item).filter(Item.location_id == location.id).all()
        enemies = (
            self.db.query(Enemy)
            .filter(Enemy.location_id == location.id, Enemy.is_alive.is_(True))
            .all()
        )

        message = f"{location.name}\n\n{location.description}"

        # List available exits
        exits = []
        if location.north_id:
            exits.append("north")
        if location.south_id:
            exits.append("south")
        if location.east_id:
            exits.append("east")
        if location.west_id:
            exits.append("west")
        if location.up_id:
            exits.append("up")
        if location.down_id:
            exits.append("down")

        if exits:
            message += f"\n\nExits: {', '.join(exits)}"

        if items:
            item_names = ", ".join([str(item.name) for item in items])
            message += f"\n\nYou see: {item_names}"

        if enemies:
            enemy_names = ", ".join([str(enemy.name) for enemy in enemies])
            message += f"\n\n⚔️ Enemies: {enemy_names}"

        return GameCommandResponse(
            success=True,
            message=message,
            location=location,  # type: ignore[arg-type]
            items=items,  # type: ignore[arg-type]
            enemies=enemies,  # type: ignore[arg-type]
        )

    def _handle_inventory(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle INVENTORY command to list player's items."""
        inventory = (
            self.db.query(PlayerInventory)
            .filter(PlayerInventory.player_id == game_state.player_id)
            .all()
        )

        if not inventory:
            return GameCommandResponse(
                success=True,
                message="Your inventory is empty.",
                inventory=[],
            )

        message = "Your inventory:\n\n"
        for inv_item in inventory:
            item = inv_item.item
            equipped_str = " (equipped)" if inv_item.equipped else ""
            quantity_str = f" x{inv_item.quantity}" if inv_item.quantity > 1 else ""
            message += f"- {item.name}{quantity_str}{equipped_str}\n"

        return GameCommandResponse(
            success=True,
            message=message,
            inventory=inventory,  # type: ignore[arg-type]
        )

    def _handle_take(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle TAKE command to pick up items."""
        item_name = match.group(1).strip()

        # Find item at current location
        item = (
            self.db.query(Item)
            .filter(
                Item.location_id == game_state.current_location_id,
                Item.name.ilike(f"%{item_name}%"),
            )
            .first()
        )

        if not item:
            return GameCommandResponse(
                success=False,
                message=f"There is no '{item_name}' here.",
            )

        if not item.is_takeable:
            return GameCommandResponse(
                success=False,
                message=f"You cannot take the {item.name}.",
            )

        # Add to player inventory
        existing_inv = (
            self.db.query(PlayerInventory)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                PlayerInventory.item_id == item.id,
            )
            .first()
        )

        if existing_inv:
            # Player already has this item - don't allow taking it again
            return GameCommandResponse(
                success=False,
                message=f"You already have the {item.name}.",
            )
        else:
            new_inv = PlayerInventory(
                player_id=game_state.player_id,
                item_id=item.id,
                quantity=1,
            )
            self.db.add(new_inv)

        # Remove item from location (for all items, not just unique ones)
        # This prevents the same item instance from being taken multiple times
        item.location_id = None  # type: ignore[assignment]

        return GameCommandResponse(
            success=True,
            message=f"You take the {item.name}.",
        )

    def _handle_stats(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle STATS command to show player statistics."""
        message = f"""
Character: {game_state.player.character_name}
Health: {game_state.health}/{game_state.max_health}
Level: {game_state.current_level}/3
Enemies Defeated: {game_state.enemies_defeated}
Bosses Defeated: {game_state.bosses_defeated}
        """.strip()

        return GameCommandResponse(
            success=True,
            message=message,
            game_state=game_state,
        )

    def _handle_help(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle HELP command."""
        message = """
Available Commands:

MOVEMENT:
  GO NORTH/SOUTH/EAST/WEST/UP/DOWN - Move in a direction

OBSERVATION:
  LOOK - Look around the current area
  EXAMINE [item] - Examine something closely
  INVENTORY - Check your inventory

INTERACTION:
  TAKE [item] - Pick up an item
  USE [item] - Use a potion or activate a magic item
  EQUIP [item] - Equip a weapon or armor

COMBAT:
  ATTACK [enemy] - Attack an enemy
  FLEE - Attempt to escape from enemies

SYSTEM:
  STATS - Show your character stats
  HELP - Show this message

TIPS:
  - Equip weapons and armor to increase your combat effectiveness
  - Activate magic items before facing powerful bosses
  - Some enemies require special items to defeat
        """.strip()

        return GameCommandResponse(
            success=True,
            message=message,
        )

    def _handle_attack(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle ATTACK command for combat."""
        enemy_name = match.group(1).strip()

        # Find enemy at current location
        enemy = (
            self.db.query(Enemy)
            .filter(
                Enemy.location_id == game_state.current_location_id,
                Enemy.name.ilike(f"%{enemy_name}%"),
                Enemy.is_alive.is_(True),
            )
            .first()
        )

        if not enemy:
            return GameCommandResponse(
                success=False,
                message=f"There is no '{enemy_name}' here to attack.",
            )

        # Check if this is a boss that requires special items
        if enemy.is_boss:
            # Get all required items for bosses
            required_items = (
                self.db.query(Item).filter(Item.required_for_boss.is_(True)).all()
            )

            # Check if player has any required items equipped
            player_has_required = False
            for req_item in required_items:
                inv = (
                    self.db.query(PlayerInventory)
                    .filter(
                        PlayerInventory.player_id == game_state.player_id,
                        PlayerInventory.item_id == req_item.id,
                        PlayerInventory.equipped.is_(True),
                    )
                    .first()
                )
                if inv:
                    player_has_required = True
                    break

            if not player_has_required and required_items:
                return GameCommandResponse(
                    success=False,
                    message=(
                        f"The {enemy.name} is too powerful! Your attacks seem ineffective.\n\n"
                        "You sense that you need powerful magical artifacts to stand a chance "
                        "against such a formidable foe. Explore the area to find items that can "
                        "aid you in this battle."
                    ),
                )

        # Calculate player damage based on equipped items
        player_damage = 10  # Base damage

        # Add weapon damage
        weapon = (
            self.db.query(PlayerInventory)
            .join(Item)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                PlayerInventory.equipped.is_(True),
                Item.item_type == ItemType.WEAPON,
            )
            .first()
        )
        if weapon and weapon.item.damage:
            player_damage += weapon.item.damage

        # Add magic power from equipped magic items
        magic_items = (
            self.db.query(PlayerInventory)
            .join(Item)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                PlayerInventory.equipped.is_(True),
                Item.item_type == ItemType.MAGIC,
            )
            .all()
        )
        for magic_inv in magic_items:
            if magic_inv.item.magic_power:
                player_damage += magic_inv.item.magic_power

        # Player attacks first
        enemy.health -= player_damage  # type: ignore[assignment]

        message = f"You attack the {enemy.name} for {player_damage} damage!"

        # Check if enemy is defeated
        if enemy.health <= 0:
            enemy.is_alive = False  # type: ignore[assignment]
            game_state.enemies_defeated += 1  # type: ignore[assignment]

            if enemy.is_boss:
                game_state.bosses_defeated += 1  # type: ignore[assignment]
                message += f"\n\n🎉 Victory! You have defeated the {enemy.name}!"

                # Advance to next level if boss defeated
                if game_state.current_level < 3:
                    game_state.current_level += 1  # type: ignore[assignment]
                    message += f"\n\nYou advance to Level {game_state.current_level}!"
            else:
                message += f"\n\nThe {enemy.name} is defeated!"

            return GameCommandResponse(
                success=True,
                message=message,
                game_state=game_state,
            )

        # Enemy counter-attacks
        player_defense = 0

        # Add armor defense
        armor = (
            self.db.query(PlayerInventory)
            .join(Item)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                PlayerInventory.equipped.is_(True),
                Item.item_type == ItemType.ARMOR,
            )
            .first()
        )
        if armor and armor.item.defense:
            player_defense += armor.item.defense

        # Add defense from magic items
        for magic_inv in magic_items:
            if magic_inv.item.defense:
                player_defense += magic_inv.item.defense

        enemy_damage = max(1, int(enemy.damage) - player_defense)
        game_state.health -= enemy_damage  # type: ignore[assignment]
        message += f"\n\nThe {enemy.name} attacks you for {enemy_damage} damage!"

        if player_defense > 0:
            message += f" (reduced by {player_defense} defense)"

        message += f"\n\nYour health: {game_state.health}/{game_state.max_health}"
        message += f"\n{enemy.name} health: {enemy.health}"

        # Check if player is defeated
        if game_state.health <= 0:
            game_state.health = game_state.max_health  # type: ignore[assignment]
            # fmt: off
            game_state.current_location_id = settings.STARTING_LOCATION_ID  # type: ignore[assignment]  # noqa: E501
            # fmt: on
            message += (
                "\n\n💀 You have been defeated! "
                "You awaken back at the starting location."
            )

        return GameCommandResponse(
            success=True,
            message=message,
            game_state=game_state,
        )

    def _handle_flee(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle FLEE command to escape from combat."""
        # Find available exits
        location = game_state.current_location
        exits = []

        if location.north_id:
            exits.append(("north", location.north_id))
        if location.south_id:
            exits.append(("south", location.south_id))
        if location.east_id:
            exits.append(("east", location.east_id))
        if location.west_id:
            exits.append(("west", location.west_id))

        if not exits:
            return GameCommandResponse(
                success=False,
                message="There is nowhere to flee!",
            )

        # Flee to a random exit
        import random

        direction, new_location_id = random.choice(exits)

        game_state.current_location_id = new_location_id
        new_location = (
            self.db.query(Location).filter(Location.id == new_location_id).first()
        )

        if new_location is None:
            return GameCommandResponse(
                success=False,
                message="Error: could not find location.",
            )

        return GameCommandResponse(
            success=True,
            message=f"You flee {direction} to {new_location.name}!",
            location=new_location,  # type: ignore[arg-type]
        )

    def _handle_examine(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle EXAMINE command to look at items closely."""
        target_name = match.group(1).strip()

        # Check location for item
        item = (
            self.db.query(Item)
            .filter(
                Item.location_id == game_state.current_location_id,
                Item.name.ilike(f"%{target_name}%"),
            )
            .first()
        )

        # Check inventory if not found
        if not item:
            inv_item = (
                self.db.query(PlayerInventory)
                .join(Item)
                .filter(
                    PlayerInventory.player_id == game_state.player_id,
                    Item.name.ilike(f"%{target_name}%"),
                )
                .first()
            )
            if inv_item:
                item = inv_item.item

        if not item:
            return GameCommandResponse(
                success=False,
                message=f"You don't see any '{target_name}' to examine.",
            )

        message = f"{item.name}\n\n{item.description}"

        if item.damage > 0:
            message += f"\nDamage: {item.damage}"
        if item.defense > 0:
            message += f"\nDefense: {item.defense}"
        if item.healing > 0:
            message += f"\nHealing: {item.healing}"
        if item.magic_power > 0:
            message += f"\nMagic Power: {item.magic_power}"

        return GameCommandResponse(
            success=True,
            message=message,
        )

    def _handle_use(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle USE command for consumable items and magic items."""
        item_name = match.group(1).strip()

        # Find item in inventory
        inv_item = (
            self.db.query(PlayerInventory)
            .join(Item)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                Item.name.ilike(f"%{item_name}%"),
            )
            .first()
        )

        if not inv_item:
            return GameCommandResponse(
                success=False,
                message=f"You don't have any '{item_name}' in your inventory.",
            )

        item = inv_item.item

        # Handle consumables (healing potions, etc.)
        if item.item_type == ItemType.CONSUMABLE:
            if item.healing > 0:
                old_health = game_state.health
                game_state.health = min(  # type: ignore[assignment]
                    game_state.max_health, game_state.health + item.healing
                )
                healed = game_state.health - old_health

                # Remove item from inventory
                if inv_item.quantity > 1:
                    inv_item.quantity -= 1  # type: ignore[assignment]
                else:
                    self.db.delete(inv_item)

                return GameCommandResponse(
                    success=True,
                    message=f"You use the {item.name} and restore {healed} health!",
                    game_state=game_state,
                )

        # Handle magic items
        if item.item_type == ItemType.MAGIC:
            # Check if already equipped
            if inv_item.equipped:
                return GameCommandResponse(
                    success=False,
                    message=f"The {item.name} is already active and empowering you.",
                )

            # Activate the magic item by equipping it
            inv_item.equipped = True  # type: ignore[assignment]

            message = f"You activate the {item.name}! "
            if item.magic_power > 0:
                message += f"You feel arcane energy flow through you (+{item.magic_power} magic power)."
            if item.defense > 0:
                message += (
                    f" A protective aura surrounds you (+{item.defense} defense)."
                )

            if item.required_for_boss:
                message += "\n\n✨ This powerful artifact will be essential when facing mighty foes!"

            return GameCommandResponse(
                success=True,
                message=message,
                game_state=game_state,
            )

        return GameCommandResponse(
            success=False,
            message=f"You cannot use the {item.name} right now.",
        )

    def _handle_equip(
        self, game_state: GameState, match: re.Match
    ) -> GameCommandResponse:
        """Handle EQUIP command for weapons and armor."""
        item_name = match.group(1).strip()

        # Find item in inventory
        inv_item = (
            self.db.query(PlayerInventory)
            .join(Item)
            .filter(
                PlayerInventory.player_id == game_state.player_id,
                Item.name.ilike(f"%{item_name}%"),
            )
            .first()
        )

        if not inv_item:
            return GameCommandResponse(
                success=False,
                message=f"You don't have any '{item_name}' in your inventory.",
            )

        item = inv_item.item

        if item.item_type not in [ItemType.WEAPON, ItemType.ARMOR]:
            return GameCommandResponse(
                success=False,
                message=f"You cannot equip the {item.name}.",
            )

        # Unequip other items of the same type
        self.db.query(PlayerInventory).filter(
            PlayerInventory.player_id == game_state.player_id,
            PlayerInventory.item_id == Item.id,
            Item.item_type == item.item_type,
        ).update({PlayerInventory.equipped: False})

        # Equip this item
        inv_item.equipped = True  # type: ignore[assignment]

        return GameCommandResponse(
            success=True,
            message=f"You equip the {item.name}.",
        )

    # ========================================================================
    # Helper Methods
    # ========================================================================

    def _get_game_state(self, player_id: int) -> Optional[GameState]:
        """Get the game state for a player."""
        return self.db.query(GameState).filter(GameState.player_id == player_id).first()

    def reset_player_game(self, player_id: int) -> None:
        """Reset a player's game to the beginning."""
        game_state = self._get_game_state(player_id)
        if game_state:
            # Reset game state
            # fmt: off
            game_state.current_location_id = settings.STARTING_LOCATION_ID  # type: ignore[assignment]  # noqa: E501
            # fmt: on
            game_state.health = settings.STARTING_HEALTH  # type: ignore[assignment]
            game_state.max_health = settings.STARTING_HEALTH  # type: ignore[assignment]
            game_state.current_level = 1  # type: ignore[assignment]
            game_state.enemies_defeated = 0  # type: ignore[assignment]
            game_state.bosses_defeated = 0  # type: ignore[assignment]
            game_state.is_completed = False  # type: ignore[assignment]
            game_state.completed_at = None  # type: ignore[assignment]

            # Clear inventory
            self.db.query(PlayerInventory).filter(
                PlayerInventory.player_id == player_id
            ).delete()

            # Reset enemies
            self.db.query(Enemy).update({Enemy.is_alive: True})

            # Reset items to their original locations
            items = self.db.query(Item).all()
            for item in items:
                if item.original_location_id:
                    item.location_id = item.original_location_id  # type: ignore[assignment]

            self.db.commit()
