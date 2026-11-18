import pygame
from pygame.math import Vector2

from ..assets import AssetManager
from .character import Character
from .projectile import Projectile
from .weapon import Shotgun, Weapon


class Knight(Character):
    """The player: moves with WASD / arrow keys and carries a weapon aimed at the mouse."""

    MAX_HEALTH = 100
    SPEED = 230.0
    INVULNERABLE_TIME = 0.7
    HEALTH_BAR_COLOR = (70, 200, 90)

    CONTROLS = {
        pygame.K_w: Vector2(0, -1), pygame.K_UP: Vector2(0, -1),
        pygame.K_s: Vector2(0, 1), pygame.K_DOWN: Vector2(0, 1),
        pygame.K_a: Vector2(-1, 0), pygame.K_LEFT: Vector2(-1, 0),
        pygame.K_d: Vector2(1, 0), pygame.K_RIGHT: Vector2(1, 0),
    }

    def __init__(self, assets: AssetManager, position, bounds: pygame.Rect):
        self._facing_right = assets.image("knight")
        self._facing_left = pygame.transform.flip(self._facing_right, True, False)
        super().__init__(self._facing_right, position)
        self.bounds = bounds
        self.weapon: Weapon = Shotgun(self, assets)

    def movement_direction(self) -> Vector2:
        keys = pygame.key.get_pressed()
        return sum((vec for key, vec in self.CONTROLS.items() if keys[key]), Vector2())

    def _constrain(self) -> None:
        half_w, half_h = self.rect.width / 2, self.rect.height / 2
        self.position.x = max(self.bounds.left + half_w, min(self.bounds.right - half_w, self.position.x))
        self.position.y = max(self.bounds.top + half_h, min(self.bounds.bottom - half_h, self.position.y))

    def aim_at(self, point) -> None:
        self.weapon.aim_at(point)
        self.image = self._facing_left if abs(self.weapon.angle) > 90 else self._facing_right

    def fire(self) -> list[Projectile]:
        return self.weapon.trigger()

    def update(self, dt: float) -> None:
        super().update(dt)
        self.weapon.update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        self.weapon.draw(surface)
