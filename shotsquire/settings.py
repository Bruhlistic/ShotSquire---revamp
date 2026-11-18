"""Global, game-wide settings. Per-entity stats live as class attributes on the entity classes."""
from pathlib import Path

TITLE = "ShotSquire"
SCREEN_SIZE = (960, 640)
FPS = 60
MAX_FRAME_TIME = 0.05  # clamp dt so a stalled frame can't teleport things

ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"
