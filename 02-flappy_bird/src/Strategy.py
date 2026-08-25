from typing import Optional
from abc import ABC, abstractmethod

from gale.input_handler import InputData

from src.World import World
from src.Bird import Bird
from src.LogPair import LogPair
import settings

class Strategy(ABC):
    @abstractmethod
    def update_obstacles(self, world: World, dt: float) -> None:
        pass

    @abstractmethod
    def update_bird(self, bird: Bird, dt: float) -> None:
        pass

class EasyStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update_obstacles(dt)
    
    def update_bird(self, bird: Bird, dt: float) -> None:
        bird.update(dt)

class HardStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update_obstacles(dt)
    
    def update_bird(self, bird: Bird, dt: float) -> None:
        bird.update(dt)

        bird.vx = 0

        if bird.movingRight:
            bird.vx = settings.HORIZONTAL_SPEED
        elif bird.movingLeft:
            bird.vx = -settings.HORIZONTAL_SPEED

        bird.x += bird.vx * dt
