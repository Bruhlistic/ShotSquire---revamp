from pygame.math import Vector2

from ..assets import AssetManager
from .character import Character


class Monster(Character):
    """Chases a target and hurts it on contact. New monster types only need to override stats."""

    MAX_HEALTH = 30
    SPEED = 95.0
    CONTACT_DAMAGE = 10
    ATTACK_COOLDOWN = 0.8
    SCORE = 10
    SCALE = 1.0  # sprite size multiplier

    def __init__(self, assets: AssetManager, position, target: Character):
        super().__init__(assets.image("monster", self.SCALE), position)
        self.target = target
        self._attack_cooldown = 0.0

    def movement_direction(self) -> Vector2:
        return self.target.position - self.position

    def try_attack(self, target: Character) -> bool:
        if self._attack_cooldown > 0:
            return False
        self._attack_cooldown = self.ATTACK_COOLDOWN
        return target.take_damage(self.CONTACT_DAMAGE)

    def update(self, dt: float) -> None:
        self._attack_cooldown = max(0.0, self._attack_cooldown - dt)
        super().update(dt)


class Imp(Monster):
    """Small, fast and fragile."""

    MAX_HEALTH = 12
    SPEED = 165.0
    CONTACT_DAMAGE = 5
    SCORE = 15
    SCALE = 0.75


class Brute(Monster):
    """Big, slow and hits hard."""

    MAX_HEALTH = 90
    SPEED = 60.0
    CONTACT_DAMAGE = 25
    ATTACK_COOLDOWN = 1.2
    KNOCKBACK_DECAY = 14.0  # shrugs off knockback faster
    SCORE = 40
    SCALE = 1.6
