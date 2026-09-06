import pygame
from gale.timer import Timer
from src.GameItem import GameItem
import settings

class SpecialBlock:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 16 
        self.height = 16

        self.image = settings.TEXTURES["block"]

        self.is_empty = False
        self.active = True
        self.collidable = True

    def hit(self, level) -> None:
        if self.is_empty:
            return
            
        self.is_empty = True
        self.image = settings.TEXTURES["e_block"]
        
        settings.SOUNDS["key"].play()

        key = Key(self.x, self.y - 1)
        level.items.append(key)
        
        # Animación de nacimiento hacia arriba
        Timer.tween(
            0.5,
            [(key, {"y": self.y - 16})],
            on_finish=lambda: setattr(key, 'collidable', True)
        )

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_collide(self, player) -> None:
        dx = (player.x + player.width / 2) - (self.x + self.width / 2)
        dy = (player.y + player.height / 2) - (self.y + self.height / 2)

        overlap_x = (player.width / 2 + self.width / 2) - abs(dx)
        overlap_y = (player.height / 2 + self.height / 2) - abs(dy)

        if overlap_x < overlap_y:
            if dx < 0:
                player.x = self.x - player.width  # Viene por la izquierda
            else:
                player.x = self.x + self.width    # Viene por la derecha
        else:
            if dy < 0:
                player.y = self.y - player.height # Aterrizando encima
                player.vy = 0
                player.change_state("idle")
            else:
                player.y = self.y + self.height   # Golpeando desde abajo
                player.vy = 0
                self.hit(player.game_level)

    def on_consume(self, player) -> None:
        pass

    def render(self, surface: pygame.Surface, camera) -> None:
        if self.active:
            base_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            dest = camera.apply(base_rect)

            surface.blit(self.image, dest)

class Key:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.image = settings.TEXTURES["key"].convert_alpha()
        
        self.active = True
        self.collidable = False
        self.consumable = True 

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def on_collide(self, player) -> None:
        self.active = False
        pygame.mixer.music.stop()
        settings.SOUNDS["victory"].play()

    def on_consume(self, player):
        pass

    def render(self, surface: pygame.Surface, camera) -> None:
        if self.active:
            base_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            dest = camera.apply(base_rect)

            surface.blit(self.image, dest)