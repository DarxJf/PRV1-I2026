import pygame

import settings

class PowerUp():
    def __init__(self, x: float, y: float, height: float, width: float):
        self.x: float = x
        self.y: float = y
        self.height: float = height
        self.width: float = width
        self.active: bool = True

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width, self.height)

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        pass

class Ghost(PowerUp):
    def __init__(self, x, y, height, width):
        super().__init__(x, y, height, width)

    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt
    
    def render(self, surface):
        surface.blit(settings.TEXTURES["ghost"], self.get_rect())