"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.powerups.LineClear import LineClear
from src.powerups.NukeColor import NukeColor

class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.level * 1.25 * 1000

        # Fundido en negro
        self.overlay_alpha = 0
        self.overlay_surface = pygame.Surface(
            (settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), 
            pygame.SRCALPHA
        )
        self.overlay_surface.fill((0, 0, 0)) # Negro puro

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        # self.line_clear_fac: Factory = Factory(LineClear)
        """
        Factory inyecta un "x" e "y" siempre en toda instancia, si mi clase
        necesita una "i" y "j", Factory de todas formas dira que es una "x" e
        "y"
        """

        def decrement_timer():
            self.timer -= 1

            # Play warning sound on timer if we get low
            if self.timer <= 5:
                settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

        if not self.board.has_matches():
            # Disparamos la misma animación de fundido a negro
            self._trigger_shuffle_animation()
        else:
            # Si sí hay jugadas, activamos al jugador normalmente
            self.active = True

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.highlighted_tile:
            x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
            y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

        if self.overlay_alpha > 0:
            self.overlay_surface.set_alpha(int(self.overlay_alpha))
            surface.blit(self.overlay_surface, (0, 0))

            if self.overlay_alpha > 200 and hasattr(self, 'shuffle_text'):
                import math
                font = settings.FONTS["medium"]
                
                # Ancho total para centrar la palabra
                total_width = sum([font.size(char)[0] for char in self.shuffle_text])
                start_x = (settings.VIRTUAL_WIDTH - total_width) // 2
                
                current_x = start_x
                
                # Usamos el tiempo real de pygame para que la onda de movimiento fluya
                time_now = pygame.time.get_ticks() / 150.0 
                
                for i, char in enumerate(self.shuffle_text):
                    # Movimiento vertical oscilatorio usando seno
                    offset_y = math.sin(time_now + i) * 5 
                    
                    # Dibujamos la letra con su respectivo movimiento
                    char_surface = font.render(char, True, (255, 255, 255))
                    surface.blit(char_surface, (current_x, (settings.VIRTUAL_HEIGHT // 2) + offset_y))
                    
                    # Avanzamos x para la siguiente letra
                    current_x += font.size(char)[0]

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click":
            pos_x, pos_y = input_data.position
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            i = (pos_y - self.board.y) // settings.TILE_SIZE
            j = (pos_x - self.board.x) // settings.TILE_SIZE

            if input_data.pressed:
                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                    if getattr(self, 'active', True):
                        self.dragged_tile = self.board.tiles[i][j]
                        self.dragged_i = i
                        self.dragged_j = j
                        if not self.highlighted_tile:
                            self.highlighted_tile = True
                            self.highlighted_i1 = self.dragged_i
                            self.highlighted_j1 = self.dragged_j
                        

            elif input_data.released:
                if hasattr(self, 'dragged_tile') and self.dragged_tile is not None:
                    if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:

                        di = abs(i - self.dragged_i)
                        dj = abs(j - self.dragged_j)
                        self.highlighted_i2 = i
                        self.highlighted_j2 = j

                        if di == 0 and dj == 0:
                            if self.dragged_tile is not None and getattr(self.dragged_tile, 'is_powerup', False):
                                self.active = False
                                act_tile = self.dragged_tile
                            
                                d_tiles = act_tile.activate(self.board)

                                settings.SOUNDS["nuke"].stop()
                                settings.SOUNDS["nuke"].play()
                            
                                self.score += len(d_tiles) * 50
                                self.board.matches.append(d_tiles)
                                self.board.remove_matches()
                            
                                falling_tiles = self.board.get_falling_tiles()
                            
                                Timer.tween(
                                    0.5,
                                    falling_tiles,
                                    on_finish=lambda: self._calculate_matches(
                                        [item[0] for item in falling_tiles], -1, -1
                                    ),
                                )

                                act_tile = None
                                return
                        elif di <= 1 and dj <= 1 and di != dj:
                            self.active = False
                            tile1 = self.dragged_tile
                            tile2 = self.board.tiles[i][j]

                            def undo():
                                (
                                    self.board.tiles[tile1.i][tile1.j],
                                    self.board.tiles[tile2.i][tile2.j],
                                ) = (
                                    self.board.tiles[tile2.i][tile2.j],
                                    self.board.tiles[tile1.i][tile1.j],
                                )
                            
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                    tile2.i, tile2.j, tile1.i, tile1.j,
                                )

                                tile1.x = tile1.j * settings.TILE_SIZE
                                tile1.y = tile1.i * settings.TILE_SIZE
                                tile2.x = tile2.j * settings.TILE_SIZE
                                tile2.y = tile2.i * settings.TILE_SIZE

                                self.active = True

                            def arrive():
                                tile1 = self.board.tiles[self.dragged_i][self.dragged_j]
                                tile2 = self.board.tiles[i][j]

                                (
                                    self.board.tiles[tile1.i][tile1.j],
                                    self.board.tiles[tile2.i][tile2.j],
                                ) = (
                                    self.board.tiles[tile2.i][tile2.j],
                                    self.board.tiles[tile1.i][tile1.j],
                                )
                            
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                    tile2.i, tile2.j, tile1.i, tile1.j,
                                )

                                match = self._calculate_matches([tile1, tile2], i, j)
                                if not match:
                                    Timer.tween(
                                        0.25,
                                        [
                                            (tile1, {"x": tile2.x, "y": tile2.y}),
                                            (tile2, {"x": tile1.x, "y": tile1.y}),
                                        ],
                                        on_finish=undo,
                                    )
                                    

                            Timer.tween(
                                0.25,
                                [
                                    (tile1, {"x": tile2.x, "y": tile2.y}),
                                    (tile2, {"x": tile1.x, "y": tile1.y}),
                                ],
                                on_finish=arrive,
                            )
                        else:
                            Timer.tween(
                                0.25,
                                [
                                    (self.dragged_tile, {
                                        "x": self.dragged_j * settings.TILE_SIZE, 
                                        "y": self.dragged_i * settings.TILE_SIZE
                                    })
                                ]
                            )
                    else:
                        Timer.tween(
                            0.25,
                            [
                                (self.dragged_tile, {
                                    "x": self.dragged_j * settings.TILE_SIZE, 
                                    "y": self.dragged_i * settings.TILE_SIZE
                                })
                            ]
                        )

                self.dragged_tile = None
                self.highlighted_tile = False

    def _calculate_matches(self, tiles: List, last_i: int, last_j: int) -> bool:
        matches = self.board.calculate_matches_for(tiles)

        if matches is None:
            
            if last_i == -1 and last_j == -1:
                if not self.board.has_matches():
                    self._trigger_shuffle_animation()
                    return False
                else:
                    self.active = True
            return False

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        power_up_act = False

        for match in matches:
            old_len = len(match) # Evita que LineClear active Nuke

            extra_tiles = []
            for tile in match:
                if getattr(tile, 'is_powerup', False):
                    extra_tiles.extend(tile.activate(self.board))

                    settings.SOUNDS["nuke"].stop()
                    settings.SOUNDS["nuke"].play()

            for tile in extra_tiles:
                if tile not in match and tile is not None:
                    match.append(tile)

            self.score += len(match) * 50

            spawn_i = last_i
            spawn_j = last_j

            for moved_tile in tiles:
                if moved_tile in match:
                    spawn_i = moved_tile.i
                    spawn_j = moved_tile.j
                    break

            if spawn_j == -1 and spawn_i == -1:
                spawn_i = match[0].i
                spawn_j = match[0].j

            if old_len >= 5:
                color = match[0].color
            
                self.board.remove_matches()
            
                power_up = NukeColor(spawn_i, spawn_j, color, 5)
                self.board.tiles[spawn_i][spawn_j] = power_up
            
                power_up_act = True
            
                break

            if old_len == 4:
                color = match[0].color

                self.board.remove_matches()

                power_up = LineClear(spawn_i, spawn_j, color, 5)
                self.board.tiles[spawn_i][spawn_j] = power_up

                power_up_act = True

                break

        if not power_up_act:
            self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        # if not self.board.has_matches():
        #     self._trigger_shuffle_animation()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles], -1, -1
            ),
        )

        return True

    def _trigger_shuffle_animation(self) -> None:
        """Inicia la coreografía de reorganización."""
        self.active = False

        # Timer.paused = True

        # 2. Preparamos el texto que vamos a dibujar
        self.shuffle_text = "Barajeando"
        
        Timer.tween(
            1,
            [(self, {"overlay_alpha": 255})],
            on_finish=self._reorganize_in_the_dark
        )

    def _reorganize_in_the_dark(self) -> None:
        """Mezcla el tablero de forma instantánea mientras la pantalla está negra."""

        self.board.shuffle_board()

        Timer.tween(
            1,
            [(self, {"overlay_alpha": 0})],
            on_finish=self._finish_shuffle
        )

    def _finish_shuffle(self) -> None:
        """Devuelve el control al jugador."""
        self.active = True
        # Timer.paused = False
