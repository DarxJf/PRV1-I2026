import pygame

from gale.state import StateMachine

from src.states.entity.BaseEntityState import BaseEntityState
from src.Bow import Bow

class PlayerFireBowState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.bow = Bow()  # El arco y su fábrica listos para usarse

    def enter(self) -> None:
        # Calculamos el punto de aparición según hacia dónde mira el jugador
        direction = self.entity.direction
        x, y = self.entity.x, self.entity.y

        if direction == "left":
            x -= 8
        elif direction == "right":
            x += self.entity.width
        elif direction == "up":
            y -= 8
        elif direction == "down":
            y += self.entity.height

        # 1. Utilizamos el Factory del arco para crear la flecha
        arrow = self.bow.fire(x, y, direction)
        
        # 2. Añadimos la flecha a la lista de proyectiles de la habitación actual
        self.dungeon.current_room.projectiles.append(arrow)

        # 3. Reproducimos el sonido y la animación de disparo
        # settings.SOUNDS["arrow_shoot"].play() 
        
        # (Ajusta el nombre de la animación según las que tengas definidas)
        self.entity.change_animation(f"sword-{direction}")
        self.entity.current_animation.reset()

    def update(self, dt: float) -> None:
        self.entity.bowRequest = False

        # Cuando la animación termine, regresamos a idle
        if self.entity.current_animation.times_played > 0:
            self.entity.current_animation.times_played = 0
            self.entity.change_state("idle")

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())