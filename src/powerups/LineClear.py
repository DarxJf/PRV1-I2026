import pygame

import settings 
from src.powerups import PowerUp

class LineClear(PowerUp):
    def __init__(self, i, j, color, variety):
        super().__init__(i, j, color, variety)

        self.is_powerup = True

        self.aura_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )

        pygame.draw.rect(
            self.aura_surface,
            (255, 215, 0, 150), 
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            width=2, # Grosor del borde
            border_radius=4
        )

    def activate(self, board):
        d_tiles = []

        if self.i > 0:
            d_tiles.append(board.tiles[self.i - 1][self.j])
        if self.i < settings.BOARD_WIDTH - 1:
            d_tiles.append(board.tiles[self.i + 1][self.j])
        if self.j > 0:
            d_tiles.append(board.tiles[self.i][self.j - 1])
        if self.j < settings.BOARD_HEIGHT - 1:
            d_tiles.append(board.tiles[self.i][self.j + 1])

        final_d_tiles = [tile for tile in d_tiles if tile is not None]
        final_d_tiles.append(self)
        
        return final_d_tiles

    def render(self, surface, offset_x, offset_y) -> None:
        super().render(surface, offset_x, offset_y)

        surface.blit(self.aura_surface, (self.x + offset_x, self.y + offset_y))