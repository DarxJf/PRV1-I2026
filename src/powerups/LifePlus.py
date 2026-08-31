from typing import TypeVar

from src.powerups.PowerUp import PowerUp

class LifePlus(PowerUp):
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 2)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        play_state.lives += 1

        self.active = False