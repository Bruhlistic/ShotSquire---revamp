import pygame
from pygame.math import Vector2

from .character import Character
from .entity import Entity


class Projectile(Entity):
    """Flies in a straight line until it hits something or its lifetime runs out."""

    DAMAGE = 10
    LIFETIME = 1.0   # seconds
    KNOCKBACK = 0.0  # impulse applied to whatever it hits

    def __init__(self, image: pygame.Surface, position, velocity):
        super().__init__(image, position)
        self.velocity = Vector2(velocity)
        self._age = 0.0

    def update(self, dt: float) -> None:
        self.position += self.velocity * dt
        self._age += dt
        if self._age >= self.LIFETIME:
            self.kill()
        self._sync_rect()

    def on_hit(self, target: Character) -> None:
        target.take_damage(self.DAMAGE)
        if self.velocity.length_squared() > 0:
            target.knock_back(self.velocity.normalize() * self.KNOCKBACK)
        self.kill()


class Bullet(Projectile):
    """A single shotgun pellet: fast, short-lived, punchy."""

    SPEED = 750.0
    DAMAGE = 12
    LIFETIME = 0.4
    KNOCKBACK = 220.0
