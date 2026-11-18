from abc import ABC, abstractmethod

import pygame
from pygame.math import Vector2


class Entity(pygame.sprite.Sprite, ABC):
    """Anything that lives in the world: has an image, a float position and updates each frame."""

    def __init__(self, image: pygame.Surface, position):
        super().__init__()
        self.image = image
        self.position = Vector2(position)
        self.radius = max(image.get_size()) / 2  # used by pygame.sprite.collide_circle
        self.rect = image.get_rect(center=self.position)

    @abstractmethod
    def update(self, dt: float) -> None:
        """Advance this entity by dt seconds."""

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)

    def _sync_rect(self) -> None:
        self.rect = self.image.get_rect(center=(round(self.position.x), round(self.position.y)))
