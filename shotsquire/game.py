import pygame

from . import settings
from .assets import AssetManager
from .background import TiledBackground
from .entities import Brute, Imp, Knight, Monster
from .hud import HUD
from .spawner import MonsterSpawner


class Game:
    """Owns the window and main loop, and wires the world objects together."""

    MONSTER_ROSTER: dict[type[Monster], float] = {Monster: 6, Imp: 3, Brute: 1}

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(settings.TITLE)
        self.screen = pygame.display.set_mode(settings.SCREEN_SIZE)
        try:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_CROSSHAIR)
        except pygame.error:
            pass  # cosmetic only; some video drivers have no system cursors
        self.clock = pygame.time.Clock()
        self.arena = self.screen.get_rect()

        self.assets = AssetManager(settings.ASSET_DIR)
        self.background = TiledBackground(self.assets.image("grass"), settings.SCREEN_SIZE)
        self.hud = HUD()
        self.running = True
        self._new_round()

    def _new_round(self) -> None:
        self.knight = Knight(self.assets, self.arena.center, self.arena)
        self.monsters: pygame.sprite.Group = pygame.sprite.Group()
        self.projectiles: pygame.sprite.Group = pygame.sprite.Group()
        self.spawner = MonsterSpawner(self.assets, self.arena, self.knight, self.MONSTER_ROSTER)
        self.score = 0
        self.game_over = False

    # --- main loop -------------------------------------------------------
    def run(self) -> None:
        while self.running:
            dt = min(self.clock.tick(settings.FPS) / 1000, settings.MAX_FRAME_TIME)
            self._handle_events()
            if not self.game_over:
                self._update(dt)
            self._draw()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not self.game_over:
                self.projectiles.add(*self.knight.fire())
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.game_over:
                self._new_round()

    def _update(self, dt: float) -> None:
        self.knight.aim_at(pygame.mouse.get_pos())
        self.knight.update(dt)
        self.monsters.add(*self.spawner.update(dt))
        self.monsters.update(dt)
        self.projectiles.update(dt)
        self._resolve_collisions()
        if self.knight.is_dead:
            self.game_over = True

    def _resolve_collisions(self) -> None:
        for projectile in self.projectiles.sprites():
            monster = pygame.sprite.spritecollideany(projectile, self.monsters, pygame.sprite.collide_circle)
            if monster:
                projectile.on_hit(monster)
                if monster.is_dead:
                    self.score += monster.SCORE
                    monster.kill()

        for monster in pygame.sprite.spritecollide(self.knight, self.monsters, False, pygame.sprite.collide_circle):
            monster.try_attack(self.knight)

    def _draw(self) -> None:
        self.background.draw(self.screen)
        # Sort by y so things lower on screen are drawn in front.
        for entity in sorted([*self.monsters, self.knight], key=lambda e: e.rect.bottom):
            entity.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        self.hud.draw(self.screen, self.knight, self.score)
        if self.game_over:
            self.hud.draw_game_over(self.screen, self.score)
        pygame.display.flip()
