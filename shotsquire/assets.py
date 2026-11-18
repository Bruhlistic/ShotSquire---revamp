from pathlib import Path

import pygame


class AssetManager:
    """Loads each image once and caches it (including scaled variants)."""

    def __init__(self, directory: Path):
        self._directory = directory
        self._images: dict[tuple[str, float], pygame.Surface] = {}

    def image(self, name: str, scale: float = 1.0) -> pygame.Surface:
        key = (name, scale)
        if key not in self._images:
            if scale == 1.0:
                path = self._directory / f"{name}.png"
                self._images[key] = pygame.image.load(path).convert_alpha()
            else:
                # Nearest-neighbour scaling keeps pixel art crisp.
                self._images[key] = pygame.transform.scale_by(self.image(name), scale)
        return self._images[key]
