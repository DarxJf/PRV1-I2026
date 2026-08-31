import random
from typing import TypeVar

from gale.factory import Factory
from gale.timer import Timer

import settings
from src.Ammo import Ammo
from src.powerups.PowerUp import PowerUp


class CannonGun(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 5)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle

        paddle.cannon = True

        Timer.after(15, lambda: setattr(play_state.paddle, 'cannon', False))
        self.active = False