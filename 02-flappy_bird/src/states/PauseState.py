from typing import Optional

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Bird import Bird
from src.World import World

class PauseState(BaseState):
    def enter(self, world: World, bird: Bird, score: int, strategy) -> None:
        self.world = world
        self.bird = bird
        self.score = score
        self.strategy = strategy

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

        render_text(
            surface,
            "PAUSED",
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def exit(self):
         Timer.resume()

    def on_input(self, input_id: str, input_data: InputData) -> None:
            if input_id == "pause" and input_data.pressed:
                settings.SOUNDS["paused"].play()
                self.state_machine.change("playing", self.world, self.bird, self.strategy, self.score,)