from typing import Optional
from abc import ABC, abstractmethod

from src.World import World

class Strategy(ABC):
    @abstractmethod
    def update_obstacles(self, world: World, dt: float) -> None:
        pass

    @abstractmethod
    def update_bird(self, world: World, dt: float) -> None:
        pass

class EasyStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update_obstacles(dt)
    
    def update_bird(self, world: World, dt: float) -> None:
        world.update_bird(dt)

class HardStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update_obstacles(dt)
    
    def update_bird(self, world: World, dt: float) -> None:
        world.update_bird(dt)
