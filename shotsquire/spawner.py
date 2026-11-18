import random

import pygame

from .assets import AssetManager
from .entities import Character, Monster


class MonsterSpawner:
    """Spawns monsters just outside the arena edges, faster and faster over time.

    `roster` maps monster classes to spawn weights, so adding a new monster type
    is just another entry here."""

    INITIAL_INTERVAL = 1.5   # seconds between spawns at the start
    MIN_INTERVAL = 0.35
    INTERVAL_DECAY = 0.97    # interval multiplier after every spawn
    EDGE_MARGIN = 40         # how far outside the arena monsters appear

    def __init__(self, assets: AssetManager, arena: pygame.Rect, target: Character,
                 roster: dict[type[Monster], float]):
        self._assets = assets
        self._arena = arena
        self._target = target
        self._types = list(roster)
        self._weights = list(roster.values())
        self._interval = self.INITIAL_INTERVAL
        self._timer = self._interval

    def update(self, dt: float) -> list[Monster]:
        """Returns any monsters spawned this frame."""
        self._timer -= dt
        if self._timer > 0:
            return []
        self._interval = max(self.MIN_INTERVAL, self._interval * self.INTERVAL_DECAY)
        self._timer = self._interval
        monster_type = random.choices(self._types, self._weights)[0]
        return [monster_type(self._assets, self._random_edge_position(), self._target)]

    def _random_edge_position(self) -> tuple[float, float]:
        area, m = self._arena, self.EDGE_MARGIN
        side = random.choice(("top", "bottom", "left", "right"))
        if side == "top":
            return random.uniform(area.left, area.right), area.top - m
        if side == "bottom":
            return random.uniform(area.left, area.right), area.bottom + m
        if side == "left":
            return area.left - m, random.uniform(area.top, area.bottom)
        return area.right + m, random.uniform(area.top, area.bottom)
