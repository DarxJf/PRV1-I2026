import random
from typing import Any

import pygame

import settings

class Ammo():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 8
        self.height = 8

        self.vx = 0
        self.vy = -200

        self.texture = settings.TEXTURES["spritesheet"]
        self.frame = random.randint(0, 6)

        self.active: bool = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        self.y += self.vy * dt

    def collides(self, another: Any) -> bool:
        return self.get_collision_rect().colliderect(another.get_collision_rect())

    def render(self, surface) -> None:
        surface.blit(self.texture, (self.x, self.y), settings.FRAMES["balls"][self.frame])
    