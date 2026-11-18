import random
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

import pygame
from pygame.math import Vector2

from ..assets import AssetManager
from .projectile import Bullet, Projectile

if TYPE_CHECKING:
    from .character import Character


class Weapon(ABC):
    """A held weapon that orbits its owner, points at an aim target and fires on a cooldown.

    Subclasses implement _fire() to decide what projectiles a shot produces."""

    COOLDOWN = 0.5        # seconds between shots
    HOLD_DISTANCE = 26   # pixels from the owner's centre to the gun's centre
    RECOIL = 0.0          # knockback applied to the owner when firing

    def __init__(self, owner: "Character", image: pygame.Surface):
        self.owner = owner
        self._image = image
        self.angle = 0.0  # degrees, 0 = pointing right, positive = clockwise on screen
        self._cooldown = 0.0

    @property
    def direction(self) -> Vector2:
        return Vector2(1, 0).rotate(self.angle)

    @property
    def muzzle_position(self) -> Vector2:
        return self.owner.position + self.direction * (self.HOLD_DISTANCE + self._image.get_width() / 2)

    @property
    def can_fire(self) -> bool:
        return self._cooldown <= 0

    def aim_at(self, point) -> None:
        offset = Vector2(point) - self.owner.position
        if offset.length_squared() > 0:
            self.angle = offset.as_polar()[1]

    def update(self, dt: float) -> None:
        self._cooldown = max(0.0, self._cooldown - dt)

    def trigger(self) -> list[Projectile]:
        """Pull the trigger. Returns the projectiles created (empty while cooling down)."""
        if not self.can_fire:
            return []
        self._cooldown = self.COOLDOWN
        self.owner.knock_back(-self.direction * self.RECOIL)
        return self._fire()

    @abstractmethod
    def _fire(self) -> list[Projectile]:
        """Create the projectiles for a single shot."""

    def draw(self, surface: pygame.Surface) -> None:
        image = self._image
        if abs(self.angle) > 90:  # aiming left: flip so the gun isn't upside down
            image = pygame.transform.flip(image, False, True)
        rotated = pygame.transform.rotate(image, -self.angle)  # pygame rotates counter-clockwise
        center = self.owner.position + self.direction * self.HOLD_DISTANCE
        surface.blit(rotated, rotated.get_rect(center=center))


class Shotgun(Weapon):
    """Fires a fan of pellets."""

    COOLDOWN = 0.6
    RECOIL = 120.0
    PELLETS = 7
    SPREAD = 30.0  # total cone angle in degrees

    def __init__(self, owner: "Character", assets: AssetManager):
        super().__init__(owner, assets.image("gun"))
        self._bullet_image = assets.image("bullet")

    def _fire(self) -> list[Projectile]:
        origin = self.muzzle_position
        pellets = []
        for i in range(self.PELLETS):
            offset = -self.SPREAD / 2 + self.SPREAD * i / (self.PELLETS - 1) + random.uniform(-3, 3)
            speed = Bullet.SPEED * random.uniform(0.85, 1.15)
            pellets.append(Bullet(self._bullet_image, origin, self.direction.rotate(offset) * speed))
        return pellets
