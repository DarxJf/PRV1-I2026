import math
import random
import pygame

from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.Projectile import Projectile
from src.GameObject import GameObject
from src.Entity import Entity
import settings

class Boss(Entity):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_vulnerable = False
        self.vulnerability_timer = 0.0
        self.fire_timer = 0.0
        self.fire_interval = 5.0
        
    def take_arrow_hit(self) -> None:
        self.is_vulnerable = True
        self.vulnerability_timer = 7.0 
        print("Aturdido")
        settings.SOUNDS["hit-enemy"].play()
        self.change_state("idle") 
        
    def damage(self, dmg: int) -> None:
        if self.is_vulnerable:
            super().damage(dmg)
            self.is_vulnerable = False
            
    def update(self, dt: float, player: any = None, room: any = None) -> None:
        super().update(dt)
        
        # Descontador del tiempo de vulnerabilidad
        if self.is_vulnerable:
            self.offset_x = random.choice([-2, 0, 2])
            
            self.vulnerability_timer -= dt
            if self.vulnerability_timer <= 0:
                self.is_vulnerable = False
                self.offset_x = 0
                self.change_state("walk")

        if player is not None:
            if not self.is_vulnerable:
                self.fire_timer += dt
                if self.fire_timer >= self.fire_interval:
                    self.fire_timer = 0.0
                    self._shoot_fireball(player, room)

    def _shoot_fireball(self, player: any, room: any) -> None:
        center_x = self.x + self.width / 2
        center_y = self.y + self.height / 2

        target_x = player.x + player.width / 2
        target_y = player.y + player.height / 2

        angle = math.atan2(target_y - center_y, target_x - center_x)
 
        spawn_radius = 30.0 
        start_x = center_x + math.cos(angle) * spawn_radius
        start_y = center_y + math.sin(angle) * spawn_radius

        speed = 60.0  
        vx = math.cos(angle) * speed
        vy = math.sin(angle) * speed

        fireball_obj = GameObject(GAME_OBJECT_DEFS["fireball"], start_x, start_y)

        fireball = Projectile(fireball_obj, "custom")

        fireball.vx = vx
        fireball.vy = vy

        # Añadimos la bola de fuego a la sala
        room.projectiles.append(fireball)

        # Opcional: Reproducir sonido de fuego
        # settings.SOUNDS["fireball"].play()
