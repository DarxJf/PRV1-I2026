import pygame

import settings 
from src.powerups import PowerUp

class NukeColor(PowerUp):
    def __init__(self, i, j, color, variety):
        super().__init__(i, j, color, variety)

        self.is_powerup = True

        self.aura_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        
        pygame.draw.rect(
            self.aura_surface,
            (255, 0, 0, 244), 
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            width=5, # Grosor del borde
            border_radius=4
        )

    def activate(self, board):
        same_tiles = []

        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                act_tile = board.tiles[i][j]
                if act_tile is not None:
                    if act_tile.color == self.color:
                        same_tiles.append(act_tile)

        return same_tiles

    def render(self, surface, offset_x, offset_y):
        super().render(surface, offset_x, offset_y)
        surface.blit(self.aura_surface, (self.x + offset_x, self.y + offset_y))