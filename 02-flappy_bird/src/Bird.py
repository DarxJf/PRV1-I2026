"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class Bird.
"""

import pygame

import settings


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.vx: float = 0.0
        self.ghost_timer: float = 0.0
        self.jumping: bool = False
        self.is_ghost: bool = False
        self.movingRight: bool = False
        self.movingLeft: bool = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), self.width - 3, self.height - 3)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float) -> None:
        self.vy += settings.GRAVITY * dt

        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        if self.is_ghost:
            g_texture = settings.TEXTURES["bird"].copy()
            g_texture.set_alpha(90)
            surface.blit(g_texture, self.get_rect())
        else:
            surface.blit(settings.TEXTURES["bird"], self.get_rect())
