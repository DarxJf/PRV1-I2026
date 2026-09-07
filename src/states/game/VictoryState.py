import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer #

import settings

class VictoryState(BaseState):
    def enter(self, player) -> None:
        self.player = player

        pygame.mixer.music.load(settings.MUSIC["game-over"])
        pygame.mixer.music.play()

        self.fade_alpha = 255

        Timer.tween(1.5, [(self, {"fade_alpha": 0})])

    def exit(self) -> None:
        pygame.mixer.music.stop()

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:

            Timer.clear() 
            self.state_machine.change("start")

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        render_text(
            surface,
            "VICTORY!",
            settings.FONTS["princess"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - 48,
            settings.COLOR_TITLE,
            center=True,
        )
        
        render_text(
            surface,
            "Press Enter to continue",
            settings.FONTS["princess-small"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 + 16,
            settings.COLOR_WHITE,
            center=True,
        )

        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), 
                pygame.SRCALPHA
            )
            fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            surface.blit(fade_surface, (0, 0))