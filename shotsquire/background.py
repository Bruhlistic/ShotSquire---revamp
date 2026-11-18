import pygame


class TiledBackground:
    """Repeats a tile across the whole screen. Pre-rendered once, so drawing is a single blit."""

    def __init__(self, tile: pygame.Surface, size: tuple[int, int]):
        self._surface = pygame.Surface(size).convert()
        tile_w, tile_h = tile.get_size()
        for x in range(0, size[0], tile_w):
            for y in range(0, size[1], tile_h):
                self._surface.blit(tile, (x, y))

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self._surface, (0, 0))
