import pygame

from .entities import Character


class HUD:

    text_colour = (245, 245, 235)
    SHADOW_COLOR = (20, 20, 28)

    def __init__(self):
        self._font = pygame.font.Font(None, 32)
        self._big_font = pygame.font.Font(None, 80)

    def draw(self, surface: pygame.Surface, player: Character, score: int) -> None:
        bar = pygame.Rect(16, 16, 220, 18)
        pygame.draw.rect(surface, self.SHADOW_COLOR, bar.inflate(4, 4))
        filled = bar.copy()
        filled.width = round(bar.width * player.health / player.MAX_HEALTH)
        pygame.draw.rect(surface, (200, 50, 50), filled)
        self._text(surface, self._font, f"Score: {score}", topright=(surface.get_width() - 16, 14))

    def draw_game_over(self, surface: pygame.Surface, score: int) -> None:
        shade = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 150))
        surface.blit(shade, (0, 0))
        cx, cy = surface.get_rect().center
        self._text(surface, self._big_font, "YOU HAVE FALLEN", center=(cx, cy - 40))
        self._text(surface, self._font, f"Score: {score}   -   press R to rise again", center=(cx, cy + 20))

    def _text(self, surface, font, text, **position) -> None:
        for offset, color in (((2, 2), self.SHADOW_COLOR), ((0, 0), self.text_colour)):
            rendered = font.render(text, False, color)
            rect = rendered.get_rect(**position).move(offset)
            surface.blit(rendered, rect)
