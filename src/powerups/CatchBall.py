import random
from typing import TypeVar

from gale.timer import Timer

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class CatchBall(PowerUp):
    def __init__(self, x, y,):
        super().__init__(x, y, 7)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.paddle.catch = True
        Timer.after(10, lambda: setattr(play_state.paddle, 'catch', False))
        self.active = False
        
        