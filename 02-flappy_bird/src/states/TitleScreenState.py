"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Strategy import EasyStrategy, HardStrategy
from src.World import World


class TitleScreenState(BaseState):
    def enter(self, ) -> None:
        self.world = World(generate_logs=False)
        self.selected_option = 0

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Select a difficulty and press Enter to start!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

        # Colores dinámicos: destacamos la opción seleccionada
        # (puedes usar un color dorado/amarillo si lo tienes en settings, o blanco vs gris)
        color_easy = (255, 255, 0) if self.selected_option == 0 else settings.COLOR_WHITE
        color_hard = (255, 255, 0) if self.selected_option == 1 else settings.COLOR_WHITE

        render_text(
            surface,
            "> Easy <" if self.selected_option == 0 else "Easy",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2 - 80,
            2 * settings.VIRTUAL_HEIGHT / 3 + 40,
            color_easy,
            center=True,
            shadowed=True,
        )

        render_text(
            surface,
            "> Hard <" if self.selected_option == 1 else "Hard",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2 + 80,
            2 * settings.VIRTUAL_HEIGHT / 3 + 40,
            color_hard,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if (input_id == "Left" or input_id == "Right") and input_data.pressed:
            self.selected_option = 1 if self.selected_option == 0 else 0
            settings.SOUNDS["paused"].play()
        elif input_id == "confirm" and input_data.pressed:
            selected_strategy = EasyStrategy() if self.selected_option == 0 else HardStrategy()

            self.state_machine.change("count_down", strategy=selected_strategy)
