"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Bird import Bird
from src.World import World
from src.Strategy import Strategy


class PlayingState(BaseState):
    def enter(self, world: Optional[World] = None, bird: Optional[Bird] = None, strategy: Optional[Strategy] = None, score: int = 0) -> None:
        self.world = world if world is not None else World()
        self.world.reset(True)
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.score = score
        self.strategy = strategy

    def update(self, dt: float) -> None:
        self.strategy.update_bird(self.bird, dt)
        self.strategy.update_obstacles(self.world, dt)
        self.strategy.update_powerups(self.world, self.bird, dt)

        if not self.bird.is_ghost:
            if self.world.collides(self.bird.get_rect()):
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["hurt"].play()
                self.state_machine.change("count_down", strategy=self.strategy)
                return
        else:
            if self.bird.y >= settings.VIRTUAL_HEIGHT - 16 or self.bird.y <= 0:
                if self.world.update_scored(self.bird.get_rect()):
                    self.score += 1
                    settings.SOUNDS["score"].play()

        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def exit(self):
        Timer.clear()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()
        elif input_id == "Right":
            if input_data.pressed:
                self.bird.movingRight = True
            elif input_data.released:
                self.bird.movingRight = False
        elif input_id == "Left":
            if input_data.pressed:
                self.bird.movingLeft = True
            elif input_data.released:
                self.bird.movingLeft = False
        elif input_id == "pause" and input_data.pressed:
            settings.SOUNDS["paused"].play()
            self.state_machine.change("pause", self.world, self.bird, self.score)
