"""
Database Initialization Script

This script populates the database with the game world: locations, items,
enemies, and the complete story for The Wizard's Keep.

Educational Notes:
- Seed data is essential for testing and development
- Proper data modeling makes complex game worlds manageable
- Transactions ensure data consistency
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from app.core.database import SessionLocal, engine, Base
from app.models.models import (
    Location,
    LocationType,
    Item,
    ItemType,
    Enemy,
    EnemyType,
)


def init_database():
    """Initialize the database with game content."""
    print("🎮 Initializing The Wizard's Keep database...")
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if already initialized
        if db.query(Location).count() > 0:
            print("⚠️  Database already contains data. Skipping initialization.")
            print("   To reset, drop the database and run this script again.")
            return
        
        print("📍 Creating locations...")
        create_locations(db)
        
        print("⚔️  Creating items...")
        create_items(db)
        
        print("👹 Creating enemies...")
        create_enemies(db)
        
        print("🔒 Setting up locked doors...")
        setup_locked_doors(db)
        
        db.commit()
        print("✅ Database initialization complete!")
        print("\n🎮 Ready to play The Wizard's Keep!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def create_locations(db):
    """Create all game locations for the 3 levels."""
    
    # ========================================================================
    # LEVEL 1: The Dark Forest & Cave Entrance
    # ========================================================================
    
    locations = []
    
    # Location 1: Forest Path (Starting Location)
    loc1 = Location(
        id=1,
        name="Forest Path",
        description=(
            "You stand at the edge of a dark forest. Ancient trees loom overhead, their branches "
            "blocking out most of the sunlight. The path ahead leads north into the shadows. "
            "Behind you to the south, the safety of the village seems very far away now.\n\n"
            "Your quest is clear: find and defeat the dark wizard who dwells in the keep beyond "
            "this forest. Many have tried before you. None have returned."
        ),
        location_type=LocationType.FOREST,
        level=1,
        south_id=None,  # Can't go back
        north_id=2,
    )
    locations.append(loc1)
    
    # Location 2: Deep Forest
    loc2 = Location(
        id=2,
        name="Deep Forest",
        description=(
            "The forest grows darker here. Strange sounds echo from the undergrowth. "
            "A crude trail continues north, while the path back south leads to the forest edge. "
            "To the east, you notice a small clearing."
        ),
        location_type=LocationType.FOREST,
        level=1,
        south_id=1,
        north_id=3,
        east_id=4,
    )
    locations.append(loc2)
    
    # Location 3: Cave Entrance
    loc3 = Location(
        id=3,
        name="Cave Entrance",
        description=(
            "A dark cave entrance yawns before you like the mouth of some great beast. "
            "The forest path continues south, but your quest leads into the darkness. "
            "Torch sconces line the cave walls, though most have long since burned out."
        ),
        location_type=LocationType.CAVE,
        level=1,
        south_id=2,
        down_id=5,
    )
    locations.append(loc3)
    
    # Location 4: Forest Clearing
    loc4 = Location(
        id=4,
        name="Forest Clearing",
        description=(
            "A small clearing in the forest. Sunlight streams through a gap in the canopy. "
            "This seems like a safe place to rest. An old wooden chest sits against a tree, "
            "covered in moss and vines."
        ),
        location_type=LocationType.FOREST,
        level=1,
        west_id=2,
    )
    locations.append(loc4)
    
    # Location 5: Cave Tunnel
    loc5 = Location(
        id=5,
        name="Cave Tunnel",
        description=(
            "You descend into a damp tunnel. Water drips from the ceiling, and the air smells "
            "of earth and decay. The passage slopes downward to the north, while a ladder leads "
            "back up to the surface."
        ),
        location_type=LocationType.CAVE,
        level=1,
        up_id=3,
        north_id=6,
    )
    locations.append(loc5)
    
    # Location 6: Goblin Den
    loc6 = Location(
        id=6,
        name="Goblin Den",
        description=(
            "A large cavern opens before you. The stench is overwhelming. This is clearly "
            "a goblin lair - crude bedding and gnawed bones litter the floor. To the east, "
            "a passage leads deeper into the caves. The tunnel back south looks inviting."
        ),
        location_type=LocationType.CAVE,
        level=1,
        south_id=5,
        east_id=7,
    )
    locations.append(loc6)
    
    # Location 7: Crystal Cavern (Boss Room)
    loc7 = Location(
        id=7,
        name="Crystal Cavern",
        description=(
            "You emerge into a breathtaking cavern filled with glowing crystals. The light "
            "they cast is both beautiful and eerie. At the far end, a massive troll guards "
            "a doorway leading down. This beast must be defeated to progress."
        ),
        location_type=LocationType.CAVE,
        level=1,
        west_id=6,
        down_id=8,  # Only accessible after defeating troll
    )
    locations.append(loc7)
    
    # ========================================================================
    # LEVEL 2: The Ancient Dungeons
    # ========================================================================
    
    # Location 8: Dungeon Stairs
    loc8 = Location(
        id=8,
        name="Dungeon Stairs",
        description=(
            "Stone stairs descend into darkness. The walls are carved from ancient stone, "
            "covered in strange runes. This place is old - older than the forest above. "
            "The air is cold and still."
        ),
        location_type=LocationType.DUNGEON,
        level=2,
        up_id=7,
        down_id=9,
    )
    locations.append(loc8)
    
    # Location 9: Dungeon Hall
    loc9 = Location(
        id=9,
        name="Dungeon Hall",
        description=(
            "A long corridor stretches before you, lined with ancient cells. Most are empty, "
            "but some contain bones and rusted chains. The hall continues east and south."
        ),
        location_type=LocationType.CORRIDOR,
        level=2,
        up_id=8,
        east_id=10,
        south_id=11,
    )
    locations.append(loc9)
    
    # Location 10: Armory
    loc10 = Location(
        id=10,
        name="Ancient Armory",
        description=(
            "This room once served as an armory. Weapon racks line the walls, though most "
            "are empty or hold rusted weapons. One rack in the corner holds something that "
            "still gleams..."
        ),
        location_type=LocationType.ROOM,
        level=2,
        west_id=9,
    )
    locations.append(loc10)
    
    # Location 11: Torture Chamber
    loc11 = Location(
        id=11,
        name="Torture Chamber",
        description=(
            "You wish you hadn't entered this room. Implements of pain and suffering line "
            "the walls. This is a place of darkness. But there might be something useful here. "
            "A passage continues south."
        ),
        location_type=LocationType.ROOM,
        level=2,
        north_id=9,
        south_id=12,
    )
    locations.append(loc11)
    
    # Location 12: Prison Cells
    loc12 = Location(
        id=12,
        name="Prison Cells",
        description=(
            "Rows of cells stretch into darkness. Most are empty, but you hear movement from "
            "some. Something dangerous lurks here. The hall continues east and north."
        ),
        location_type=LocationType.DUNGEON,
        level=2,
        north_id=11,
        east_id=13,
    )
    locations.append(loc12)
    
    # Location 13: Orc Barracks
    loc13 = Location(
        id=13,
        name="Orc Barracks",
        description=(
            "This large room serves as barracks for the wizard's orc guards. Crude beds and "
            "weapons are scattered about. The orcs here are larger and better equipped than "
            "typical rabble. A heavy door to the south leads to the keep proper."
        ),
        location_type=LocationType.ROOM,
        level=2,
        west_id=12,
        south_id=14,
    )
    locations.append(loc13)
    
    # Location 14: Throne Room (Boss)
    loc14 = Location(
        id=14,
        name="Throne Room",
        description=(
            "A grand throne room, now fallen into decay. On the throne sits a massive hobgoblin "
            "warlord, the wizard's chief enforcer. He rises as you enter, drawing a wicked blade. "
            "'None shall pass,' he growls. Beyond him, stairs lead up to a locked iron door."
        ),
        location_type=LocationType.ROOM,
        level=2,
        north_id=13,
        # up_id will be set after Location 15 is created
    )
    locations.append(loc14)
    
    # ========================================================================
    # LEVEL 3: The Wizard's Keep
    # ========================================================================
    
    # Location 15: Keep Entrance
    loc15 = Location(
        id=15,
        name="Keep Entrance Hall",
        description=(
            "You ascend into the wizard's keep. The air here crackles with magical energy. "
            "Grand tapestries line the walls, depicting scenes of conquest and dark rituals. "
            "Halls lead north and east."
        ),
        location_type=LocationType.CORRIDOR,
        level=3,
        down_id=14,
        # north_id, east_id, and required_key_id will be set after all locations are created
        is_locked=True,  # Locked until player has Iron Key
    )
    locations.append(loc15)
    
    # Location 16: Library
    loc16 = Location(
        id=16,
        name="Arcane Library",
        description=(
            "Towering bookshelves filled with ancient tomes surround you. The knowledge here "
            "could take lifetimes to absorb. One book on a pedestal glows with inner light - "
            "a spellbook of great power."
        ),
        location_type=LocationType.ROOM,
        level=3,
        # south_id will be set after all locations are created
    )
    locations.append(loc16)
    
    # Location 17: Laboratory
    loc17 = Location(
        id=17,
        name="Alchemical Laboratory",
        description=(
            "Bubbling beakers and strange apparatus fill this room. The wizard's experiments "
            "are conducted here. Potions line the shelves - some might be useful. "
            "A passage continues east."
        ),
        location_type=LocationType.ROOM,
        level=3,
        # west_id will be set after all locations are created
        east_id=18,
    )
    locations.append(loc17)
    
    # Location 18: Gallery
    loc18 = Location(
        id=18,
        name="Portrait Gallery",
        description=(
            "A long gallery lined with portraits. They seem to watch you as you pass. "
            "At the end of the gallery, double doors lead north. The air here is thick "
            "with magic."
        ),
        location_type=LocationType.CORRIDOR,
        level=3,
        west_id=17,
        north_id=19,
    )
    locations.append(loc18)
    
    # Location 19: Courtyard
    loc19 = Location(
        id=19,
        name="Courtyard",
        description=(
            "An open courtyard atop the keep. The wizard's power has corrupted even the sky here - "
            "dark clouds swirl overhead, lit by flashes of purple lightning. A tower rises to the "
            "east. This is where your quest will end, one way or another."
        ),
        location_type=LocationType.COURTYARD,
        level=3,
        south_id=18,
        east_id=20,
    )
    locations.append(loc19)
    
    # Location 20: Wizard's Tower (Final Boss)
    loc20 = Location(
        id=20,
        name="The Wizard's Sanctum",
        description=(
            "You stand in the wizard's inner sanctum at the top of his tower. Arcane symbols "
            "glow on every surface. At the center of the room stands Malachar the Dark, the "
            "wizard whose evil has plagued the land for decades.\n\n"
            "'So,' he says, turning to face you. 'Another fool comes to die. I've slain "
            "a hundred heroes. You will be just one more.'\n\n"
            "This is it. The final battle."
        ),
        location_type=LocationType.TOWER,
        level=3,
        west_id=19,
    )
    locations.append(loc20)
    
    # Add all locations to database
    for loc in locations:
        db.add(loc)


def create_items(db):
    """Create all items in the game."""
    
    items = []
    
    # ========================================================================
    # Level 1 Items
    # ========================================================================
    
    # Starting area
    item1 = Item(
        name="Rusty Sword",
        description="An old sword, rusty but still serviceable. Better than nothing.",
        item_type=ItemType.WEAPON,
        damage=5,
        location_id=4,  # Forest Clearing
        original_location_id=4,
        is_takeable=True,
    )
    items.append(item1)
    
    item2 = Item(
        name="Healing Potion",
        description="A glass vial containing a red liquid. It smells medicinal.",
        item_type=ItemType.CONSUMABLE,
        healing=30,
        location_id=4,  # Forest Clearing
        original_location_id=4,
        is_takeable=True,
    )
    items.append(item2)
    
    item3 = Item(
        name="Leather Armor",
        description="Simple leather armor. Well-worn but still protective.",
        item_type=ItemType.ARMOR,
        defense=3,
        location_id=5,  # Cave Tunnel
        original_location_id=5,
        is_takeable=True,
    )
    items.append(item3)
    
    item4 = Item(
        name="Glowing Crystal",
        description=(
            "A crystal that pulses with magical light. You sense it has power that could "
            "help against strong foes."
        ),
        item_type=ItemType.MAGIC,
        magic_power=10,
        location_id=7,  # Crystal Cavern (after defeating troll)
        original_location_id=7,
        is_takeable=True,
        required_for_boss=True,
    )
    items.append(item4)
    
    # ========================================================================
    # Level 2 Items
    # ========================================================================
    
    item5 = Item(
        name="Steel Longsword",
        description="A well-crafted steel sword. Sharp and balanced.",
        item_type=ItemType.WEAPON,
        damage=15,
        location_id=10,  # Ancient Armory
        original_location_id=10,
        is_takeable=True,
    )
    items.append(item5)
    
    item6 = Item(
        name="Chainmail Armor",
        description="Heavy chainmail that provides excellent protection.",
        item_type=ItemType.ARMOR,
        defense=8,
        location_id=10,  # Ancient Armory
        original_location_id=10,
        is_takeable=True,
    )
    items.append(item6)
    
    item7 = Item(
        name="Greater Healing Potion",
        description="A large vial of healing potion. It glows with restorative magic.",
        item_type=ItemType.CONSUMABLE,
        healing=50,
        location_id=11,  # Torture Chamber
        original_location_id=11,
        is_takeable=True,
    )
    items.append(item7)
    
    item8 = Item(
        name="Iron Key",
        description="A large iron key. It must unlock something important in the keep above.",
        item_type=ItemType.KEY,
        location_id=14,  # Throne Room (after defeating boss)
        original_location_id=14,
        is_takeable=True,
        is_unique=True,
    )
    items.append(item8)
    
    # ========================================================================
    # Level 3 Items
    # ========================================================================
    
    item9 = Item(
        name="Spellbook of Power",
        description=(
            "An ancient spellbook containing powerful incantations. Reading it fills you with "
            "arcane knowledge. This will be essential against the wizard."
        ),
        item_type=ItemType.MAGIC,
        magic_power=25,
        location_id=16,  # Library
        original_location_id=16,
        is_takeable=True,
        required_for_boss=True,
    )
    items.append(item9)
    
    item10 = Item(
        name="Superior Healing Potion",
        description="The finest healing potion, glowing bright gold. Fully restores health.",
        item_type=ItemType.CONSUMABLE,
        healing=100,
        location_id=17,  # Laboratory
        original_location_id=17,
        is_takeable=True,
    )
    items.append(item10)
    
    item11 = Item(
        name="Elven Blade",
        description=(
            "A magnificent elven sword that seems to sing as it cuts through the air. "
            "It glows with an inner light and feels perfectly balanced in your hand."
        ),
        item_type=ItemType.WEAPON,
        damage=25,
        location_id=19,  # Courtyard
        original_location_id=19,
        is_takeable=True,
    )
    items.append(item11)
    
    item12 = Item(
        name="Amulet of Protection",
        description=(
            "A silver amulet inscribed with protective runes. It thrums with defensive magic."
        ),
        item_type=ItemType.MAGIC,
        defense=10,
        magic_power=15,
        location_id=19,  # Courtyard
        original_location_id=19,
        is_takeable=True,
    )
    items.append(item12)
    
    # Add all items
    for item in items:
        db.add(item)


def create_enemies(db):
    """Create all enemies in the game."""
    
    enemies = []
    
    # ========================================================================
    # Level 1 Enemies
    # ========================================================================
    
    enemy1 = Enemy(
        name="Forest Goblin",
        description="A small, vicious goblin with yellowed teeth and cruel eyes.",
        enemy_type=EnemyType.GOBLIN,
        health=20,
        damage=5,
        defense=0,
        location_id=2,  # Deep Forest
        level=1,
    )
    enemies.append(enemy1)
    
    enemy2 = Enemy(
        name="Kobold Scout",
        description="A dog-like kobold wielding a crude spear.",
        enemy_type=EnemyType.KOBOLD,
        health=15,
        damage=4,
        defense=0,
        location_id=5,  # Cave Tunnel
        level=1,
    )
    enemies.append(enemy2)
    
    enemy3 = Enemy(
        name="Goblin Warrior",
        description="A larger, better-armed goblin. It looks mean.",
        enemy_type=EnemyType.GOBLIN,
        health=30,
        damage=8,
        defense=2,
        location_id=6,  # Goblin Den
        level=1,
    )
    enemies.append(enemy3)
    
    # Level 1 Boss
    enemy4 = Enemy(
        name="Cave Troll",
        description=(
            "A massive troll, towering three times your height. Its skin is like stone, "
            "and it wields a club made from an entire tree trunk. This will be a difficult fight."
        ),
        enemy_type=EnemyType.TROLL,
        health=80,
        damage=15,
        defense=5,
        is_boss=True,
        location_id=7,  # Crystal Cavern
        level=1,
    )
    enemies.append(enemy4)
    
    # ========================================================================
    # Level 2 Enemies
    # ========================================================================
    
    enemy5 = Enemy(
        name="Dungeon Kobold",
        description="A kobold guard, better equipped than the ones above.",
        enemy_type=EnemyType.KOBOLD,
        health=25,
        damage=7,
        defense=2,
        location_id=9,  # Dungeon Hall
        level=2,
    )
    enemies.append(enemy5)
    
    enemy6 = Enemy(
        name="Gnoll Scavenger",
        description="A hyena-headed gnoll, slavering and dangerous.",
        enemy_type=EnemyType.GNOLL,
        health=35,
        damage=10,
        defense=3,
        location_id=11,  # Torture Chamber
        level=2,
    )
    enemies.append(enemy6)
    
    enemy7 = Enemy(
        name="Orc Guard",
        description="A brutish orc in heavy armor, wielding a wicked axe.",
        enemy_type=EnemyType.ORC,
        health=45,
        damage=12,
        defense=5,
        location_id=12,  # Prison Cells
        level=2,
    )
    enemies.append(enemy7)
    
    enemy8 = Enemy(
        name="Orc Berserker",
        description="A massive orc that seems to live for battle. Its eyes burn with rage.",
        enemy_type=EnemyType.ORC,
        health=50,
        damage=14,
        defense=4,
        location_id=13,  # Orc Barracks
        level=2,
    )
    enemies.append(enemy8)
    
    # Level 2 Boss
    enemy9 = Enemy(
        name="Grimtooth the Hobgoblin Warlord",
        description=(
            "The wizard's chief enforcer, a massive hobgoblin clad in dark plate armor. "
            "His sword glows with fell magic. Many heroes have fallen to his blade."
        ),
        enemy_type=EnemyType.HOBGOBLIN,
        health=120,
        damage=20,
        defense=8,
        is_boss=True,
        location_id=14,  # Throne Room
        level=2,
    )
    enemies.append(enemy9)
    
    # ========================================================================
    # Level 3 Enemies
    # ========================================================================
    
    enemy10 = Enemy(
        name="Wizard's Apprentice",
        description="A cloaked figure wielding minor magic. Still dangerous.",
        enemy_type=EnemyType.WIZARD,
        health=40,
        damage=15,
        defense=3,
        location_id=17,  # Laboratory
        level=3,
    )
    enemies.append(enemy10)
    
    enemy11 = Enemy(
        name="Arcane Guardian",
        description="A magical construct that guards the keep. It shimmers with power.",
        enemy_type=EnemyType.WIZARD,
        health=60,
        damage=18,
        defense=6,
        location_id=18,  # Gallery
        level=3,
    )
    enemies.append(enemy11)
    
    enemy12 = Enemy(
        name="Elite Orc Champion",
        description="The finest of the wizard's orc warriors, guarding the courtyard.",
        enemy_type=EnemyType.ORC,
        health=70,
        damage=20,
        defense=8,
        location_id=19,  # Courtyard
        level=3,
    )
    enemies.append(enemy12)
    
    # Final Boss
    enemy13 = Enemy(
        name="Malachar the Dark Wizard",
        description=(
            "The dark wizard himself. His eyes glow with malevolent power, and the air around "
            "him crackles with arcane energy. He has ruled through fear and dark magic for "
            "decades. This is the moment you've been preparing for. Everything comes down to this "
            "final battle."
        ),
        enemy_type=EnemyType.WIZARD,
        health=200,
        damage=30,
        defense=10,
        is_boss=True,
        location_id=20,  # Wizard's Sanctum
        level=3,
    )
    enemies.append(enemy13)
    
    # Add all enemies
    for enemy in enemies:
        db.add(enemy)


def setup_locked_doors(db):
    """Configure locked doors after locations and items are created."""
    
    # Flush pending changes first to ensure all locations and items exist
    db.flush()
    
    # Set up forward references for Level 3 locations
    location_14 = db.query(Location).filter(Location.id == 14).first()
    if location_14:
        location_14.up_id = 15
        db.add(location_14)
        print("   ✓ Connected Throne Room to Keep Entrance")
    
    location_15 = db.query(Location).filter(Location.id == 15).first()
    if location_15:
        location_15.north_id = 16
        location_15.east_id = 17
        location_15.required_key_id = 8  # Iron Key
        db.add(location_15)
        print("   ✓ Keep Entrance locked with Iron Key")
    
    location_16 = db.query(Location).filter(Location.id == 16).first()
    if location_16:
        location_16.south_id = 15
        db.add(location_16)
        print("   ✓ Connected Library to Keep Entrance")
    
    location_17 = db.query(Location).filter(Location.id == 17).first()
    if location_17:
        location_17.west_id = 15
        db.add(location_17)
        print("   ✓ Connected Laboratory to Keep Entrance")
    
    # Flush the changes
    db.flush()


if __name__ == "__main__":
    init_database()
