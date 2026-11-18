from abc import abstractmethod

import pygame
from pygame.math import Vector2

from .entity import Entity


class Character(Entity):
    """An entity with health that moves itself. Subclasses decide *where* to move
    (movement_direction) and tune behaviour through the class-level stats below."""

    MAX_HEALTH = 100
    SPEED = 100.0             # pixels / second
    INVULNERABLE_TIME = 0.0   # seconds of immunity after taking a hit
    KNOCKBACK_DECAY = 8.0     # how quickly knockback velocity fades
    FLASH_TIME = 0.1          # white hit-flash duration
    HEALTH_BAR_COLOR = (220, 50, 50)

    def __init__(self, image: pygame.Surface, position):
        super().__init__(image, position)
        self.radius *= 0.8  # sprites have transparent padding; be a little forgiving
        self.health = self.MAX_HEALTH
        self._invulnerable = 0.0
        self._flash = 0.0
        self._knockback = Vector2()

    # --- behaviour hooks -------------------------------------------------
    @abstractmethod
    def movement_direction(self) -> Vector2:
        """Direction this character wants to move this frame (any length; it gets normalised)."""

    def _constrain(self) -> None:
        """Hook to keep the character inside some area. Default: unconstrained."""

    # --- state -----------------------------------------------------------
    @property
    def is_dead(self) -> bool:
        return self.health <= 0

    def take_damage(self, amount: float) -> bool:
        """Apply damage; returns False if the hit was ignored (invulnerable / already dead)."""
        if self._invulnerable > 0 or self.is_dead:
            return False
        self.health = max(0, self.health - amount)
        self._invulnerable = self.INVULNERABLE_TIME
        self._flash = self.FLASH_TIME
        return True

    def knock_back(self, impulse: Vector2) -> None:
        self._knockback += impulse

    # --- frame -----------------------------------------------------------
    def update(self, dt: float) -> None:
        direction = self.movement_direction()
        if direction.length_squared() > 0:
            direction = direction.normalize()
        self.position += direction * self.SPEED * dt + self._knockback * dt
        self._knockback *= max(0.0, 1 - self.KNOCKBACK_DECAY * dt)
        self._invulnerable = max(0.0, self._invulnerable - dt)
        self._flash = max(0.0, self._flash - dt)
        self._constrain()
        self._sync_rect()

    def draw(self, surface: pygame.Surface) -> None:
        if self._flash > 0:
            silhouette = pygame.mask.from_surface(self.image).to_surface(
                setcolor=(255, 255, 255, 255), unsetcolor=(0, 0, 0, 0))
            surface.blit(silhouette, self.rect)
        elif self._invulnerable == 0 or int(self._invulnerable * 20) % 2 == 0:  # blink while immune
            super().draw(surface)
        if self.health < self.MAX_HEALTH:
            self._draw_health_bar(surface)

    def _draw_health_bar(self, surface: pygame.Surface) -> None:
        bar = pygame.Rect(0, 0, self.rect.width * 0.8, 4)
        bar.midbottom = (self.rect.centerx, self.rect.top - 3)
        pygame.draw.rect(surface, (30, 30, 30), bar)
        bar.width = round(bar.width * self.health / self.MAX_HEALTH)
        pygame.draw.rect(surface, self.HEALTH_BAR_COLOR, bar)
