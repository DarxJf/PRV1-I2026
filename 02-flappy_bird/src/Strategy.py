from abc import ABC, abstractmethod
import random

import pygame

from src.World import World
from src.Bird import Bird
from src.animations.animation_logs import animate_log_gap
import settings

class Strategy(ABC):
    @abstractmethod
    def update_obstacles(self, world: World, dt: float) -> None:
        pass

    @abstractmethod
    def update_bird(self, bird: Bird, dt: float) -> None:
        pass

    @abstractmethod
    def update_powerups(self, world: World, bird: Bird, dt: float) -> None:
        pass

class EasyStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update(dt)
        world.logs_spawn_timer += dt
    
        if world.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
            world.logs_spawn_timer = 0.0
            y = max(
                -settings.LOG_HEIGHT + 10,
                min(
                    world.last_log_y + random.randint(-40, 40),
                    settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                ),
            )
            world.last_log_y = y
            world.logs.append(world.log_pair_factory.create(settings.VIRTUAL_WIDTH, y))

    
    def update_bird(self, bird: Bird, dt: float) -> None:
        bird.update(dt)

    def update_powerups(self, world, bird, dt):
        pass

class HardStrategy(Strategy):
    def update_obstacles(self, world: World, dt: float) -> None:
        world.update(dt)
        world.logs_spawn_timer += dt
        if world.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS + 0.5:
            world.logs_spawn_timer = 0.0
            y = max(
                -settings.LOG_HEIGHT + 20,
                min(
                    world.last_log_y + random.randint(-40, 40),
                       settings.VIRTUAL_HEIGHT + 200 - settings.LOG_HEIGHT,
                ),
            )
            world.last_log_y = y
            world.logs.append(world.log_pair_factory.create(settings.VIRTUAL_WIDTH, y))

        for log_pair in world.logs:
            if not getattr(log_pair, "animating_gap", False):
                log_pair.animating_gap = True
                animate_log_gap(log_pair)

    def update_bird(self, bird: Bird, dt: float) -> None:
        bird.update(dt)

        bird.vx = 0

        if bird.movingRight:
            bird.vx = settings.HORIZONTAL_SPEED
        elif bird.movingLeft:
            bird.vx = -settings.HORIZONTAL_SPEED

        bird.x += bird.vx * dt

        if bird.is_ghost:
            bird.ghost_timer -= dt

            if bird.ghost_timer <= 0:
                bird.is_ghost = False
                settings.SOUNDS["ghost"].stop()
                pygame.mixer.music.play()

    def update_powerups(self, world: World, bird: Bird, dt: float):
        world.powerup_spawn_timer += dt
        if world.powerup_spawn_timer >= world.next_powerup_spawn:
            world.powerup_spawn_timer = 0.0
            world.next_powerup_spawn = random.uniform(13.0, 17.0)

            spawn_y = random.randint(50, settings.VIRTUAL_HEIGHT - 80)
            world.powerups.append(
                world.ghost_factory.create(
                    settings.VIRTUAL_WIDTH, 
                    spawn_y, 
                    {"height": 35, "width": 32}
                )
            )

        for powerup in world.powerups:
            powerup.update(dt)

            if powerup.active and bird.get_rect().colliderect(powerup.get_rect()):
                powerup.active = False
                
                bird.is_ghost = True
                bird.ghost_timer = 8.0
                
                pygame.mixer.music.pause()
                settings.SOUNDS["ghost"].play(-1)
                settings.SOUNDS["pick"].play()

        world.powerups = [p for p in world.powerups if p.active and p.x > -p.width]