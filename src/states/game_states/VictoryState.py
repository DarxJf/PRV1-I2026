import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings


class VictoryState(BaseState):
    def enter(self, current_level, player) -> None:
        self.current_level = current_level
        self.player = player
        
        # 1. Configurar el fundido a negro (fade-in)
        self.fade_alpha = 255 # Empezamos totalmente a oscuras
        
        # Animamos la transparencia de 255 a 0 en 1.5 segundos
        Timer.tween(1.5, [(self, {"fade_alpha": 0})])

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            # 2. Es importante limpiar los timers antes de cambiar de estado
            Timer.clear() 
            
            # 3. Aquí puedes manejar la lógica de ir al nivel 2, 3, etc.
            # Por ahora, te regreso a play.
            self.state_machine.change("play")

    def render(self, surface: pygame.Surface) -> None:
        # Un fondo distinto para la victoria (ej. verde oscuro)
        surface.fill((34, 139, 34))

        render_text(
            surface,
            "Level Complete!",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH // 2,
            20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )

        y = 50

        # Dibujar las monedas recolectadas
        for color, amount in self.player.coins_counter.items():
            surface.blit(
                settings.TEXTURES["tiles"],
                (settings.VIRTUAL_WIDTH // 2 - 32, y),
                settings.FRAMES["tiles"][color],
            )
            render_text(
                surface,
                "x",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2,
                y + 3,
                (255, 255, 255),
                shadowed=True,
            )
            render_text(
                surface,
                f"{amount}",
                settings.FONTS["small"],
                settings.VIRTUAL_WIDTH // 2 + 16,
                y + 3,
                (255, 255, 255),
                shadowed=True,
            )
            y += 20

        # Dibujar el puntaje final
        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            y + 10,
            (255, 255, 255),
            shadowed=True,
            center=True,
        )

        render_text(
            surface,
            "Press Enter to continue",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH // 2,
            settings.VIRTUAL_HEIGHT - 20,
            (255, 255, 255),
            center=True,
            shadowed=True,
        )
        
        # 4. Renderizar el rectángulo del fundido por encima de TODO
        if self.fade_alpha > 0:
            fade_surface = pygame.Surface(
                (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), 
                pygame.SRCALPHA
            )
            fade_surface.fill((0, 0, 0, int(self.fade_alpha)))
            surface.blit(fade_surface, (0, 0))

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "enter" and input_data.pressed:
            settings.SOUNDS["victory"].stop()
            next_level = self.current_level.level + 1
            if next_level <= settings.NUM_LEVELS:
                self.state_machine.change("play", level=next_level)
            else:
                self.state_machine.change("start")