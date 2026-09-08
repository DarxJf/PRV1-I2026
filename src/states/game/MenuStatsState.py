import pygame
from typing import Any

from gale.state import BaseState

from src.gui.Menu import Menu
from src.gui.Panel import Panel
import settings
from gale.input_handler import InputData

class MenuStatsState(BaseState):
    def enter(self, party: Any, **kwargs) -> None:
        self.party = party
        
        # Guardamos los personajes en una lista para acceder por índice (0 al 3)
        self.char_list = list(self.party.characters.values())
        
        # Modos: "char_select" -> "action_select" -> "target_select"[cite: 2]
        self.mode = "char_select" 
        self.selected_idx = 0  # 0-3 para personajes, 4 para el botón "Volver"

    # -- Lógica de Apertura de Menús --
    def _try_open_action_menu(self, char: Any) -> None:
        items = []
        
        # Filtramos para mostrar solo los poderes "verdes" (curación)
        for action in char.actions:
            if action["name"] == "Heal":
                items.append(("Curar", lambda c=char: self._on_heal_selected(c)))
            elif action["name"] == "Global Heal":
                items.append(("Cura Global", lambda c=char: self._on_global_heal_selected(c)))
        
        # Si el personaje seleccionado tiene poderes de curación, abrimos el menú
        if items:
            items.append(("Volver atras", self._cancel_action_menu))
            self.action_menu = Menu(
                x=settings.VIRTUAL_WIDTH - 130,
                y=settings.VIRTUAL_HEIGHT - 100,
                width=120,
                height=90,
                items=items,
                show_cursor=True
            )
            self.mode = "action_select"
        else:
            # Si seleccionamos un guerrero/mago sin poderes verdes, solo hacemos un sonido
            if "blip" in settings.SOUNDS:
                settings.SOUNDS["blip"].stop()
                settings.SOUNDS["blip"].play()

    def _cancel_action_menu(self) -> None:
        self.mode = "char_select"

    # -- Callbacks de Curación --
    def _on_heal_selected(self, healer_char: Any) -> None:
        self.mode = "target_select"
        items = []
        # Menú para curación individual[cite: 4]
        for char in self.char_list:
            items.append((
                f"{char.klass.capitalize()} ({char.current_hp}/{char.hp})", 
                lambda target=char: self._apply_heal(healer_char, target, is_global=False)
            ))
            
        items.append(("Cancelar", self._cancel_target_menu))
        
        self.target_menu = Menu(
            x=settings.VIRTUAL_WIDTH - 160,
            y=settings.VIRTUAL_HEIGHT - 120,
            width=150,
            height=110,
            items=items,
            show_cursor=True
        )

    def _on_global_heal_selected(self, healer_char: Any) -> None:
        # Curación global sin abrir selección de objetivo[cite: 4]
        self._apply_heal(healer_char, None, is_global=True)
        
    def _cancel_target_menu(self) -> None:
        self.mode = "action_select"

    def _apply_heal(self, healer_char: Any, target_char: Any, is_global: bool) -> None:
        action_name = "Global Heal" if is_global else "Heal"
        heal_strength = next((a["strength"] for a in healer_char.actions if a["name"] == action_name), 5)
        
        if is_global:
            for char in self.char_list:
                char.heal(heal_strength)
        else:
            target_char.heal(heal_strength)
            
        settings.SOUNDS["powerup"].stop()
        settings.SOUNDS["powerup"].play()
        
        # Volvemos al menú base después de curar
        self.mode = "char_select"

    def _exit_stats(self) -> None:
        from src.states.game.FadeInState import FadeInState
        from src.states.game.FadeOutState import FadeOutState
        # Evitar doble activación
        self.mode = "exiting"
        
        def close_and_reveal():
            self.state_machine.pop() # Sacamos el StatsMenuState
            # Apilamos FadeOut para volver de negro a transparente
            self.state_machine.push(FadeOutState(self.state_machine), color=(0, 0, 0), time=0.5)
            
        self.state_machine.push(
            FadeInState(self.state_machine),
            color=(0, 0, 0),
            time=0.5,
            on_complete=close_and_reveal
        )

    # -- Ciclo de Vida --
    def update(self, dt: float) -> None:
        if self.mode == "action_select":
            self.action_menu.update(dt)
        elif self.mode == "target_select":
            self.target_menu.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill((0, 0, 0))

        font = settings.FONTS["small"]
        
        # Renderizamos los 4 recuadros[cite: 4]
        panel_width = settings.VIRTUAL_WIDTH / 2 - 20
        panel_height = 80
        x_positions = [10, settings.VIRTUAL_WIDTH / 2 + 10]
        y_positions = [10, 100]
        
        for idx, char in enumerate(self.char_list):
            x = x_positions[idx % 2]
            y = y_positions[idx // 2]
            
            char_panel = Panel(x, y, panel_width, panel_height)
            char_panel.render(surface)
            
            # Resaltar el panel si estamos navegando y el cursor está sobre él
            if self.mode == "char_select" and self.selected_idx == idx:
                pygame.draw.rect(surface, (255, 255, 0), (x, y, panel_width, panel_height), 3, border_radius=3)
            
            # Textos de estado
            name_text = f"[{char.klass.capitalize()}] Nvl: {char.level}"
            hp_text = f"HP: {char.current_hp}/{char.hp}"
            
            surface.blit(font.render(name_text, True, (255, 255, 0)), (x + 10, y + 10))
            surface.blit(font.render(hp_text, True, (255, 255, 255)), (x + 10, y + 25))
            
            # Renderizado con transparencia paramétrica[cite: 4]
            action_x, action_y = x + 10, y + 55
            for action in char.actions:
                is_heal = action["name"] in ("Heal", "Global Heal")
                
                # Alpha value para opacidad, 255 opaco, 100 transparente[cite: 4]
                alpha = 255 if is_heal else 100 
                action_color = (100, 255, 100) if is_heal else (255, 200, 200)
                
                action_surf = font.render(action["name"], True, action_color)
                action_surf.set_alpha(alpha)
                
                surface.blit(action_surf, (action_x, action_y))
                action_x += action_surf.get_width() + 10

        # Dibujar botón inferior "Volver al Juego" para evitar usar Escape
        btn_x, btn_y = settings.VIRTUAL_WIDTH / 2 - 60, settings.VIRTUAL_HEIGHT - 35
        volver_rect = pygame.Rect(btn_x, btn_y, 120, 25)
        pygame.draw.rect(surface, (56, 56, 56), volver_rect, border_radius=3)
        if self.mode == "char_select" and self.selected_idx == 4:
            pygame.draw.rect(surface, (255, 255, 0), volver_rect, 2, border_radius=3)
            
        volver_surf = font.render("Volver al Juego", True, (255, 255, 255))
        surface.blit(volver_surf, (btn_x + 10, btn_y + 6))

        # Dibujar menús anidados si corresponden[cite: 2]
        if self.mode == "action_select":
            self.action_menu.render(surface)
        elif self.mode == "target_select":
            self.target_menu.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not input_data.pressed:
            return

        # Modo 1: Navegación de grilla (2x2 + Botón Inferior)
        if self.mode == "char_select":
            if input_id == "move_right" and self.selected_idx in (0, 2):
                self.selected_idx += 1
            elif input_id == "move_left" and self.selected_idx in (1, 3):
                self.selected_idx -= 1
            elif input_id == "move_down":
                if self.selected_idx in (0, 1): self.selected_idx += 2
                elif self.selected_idx in (2, 3): self.selected_idx = 4
            elif input_id == "move_up":
                if self.selected_idx in (2, 3): self.selected_idx -= 2
                elif self.selected_idx == 4: self.selected_idx = 2
            elif input_id in ("enter", "space"):
                if self.selected_idx == 4:
                    self._exit_stats() # Volvemos a la pausa principal
                else:
                    self._try_open_action_menu(self.char_list[self.selected_idx])
                    
        # Modo 2: Menú de habilidades del Healer[cite: 2]
        elif self.mode == "action_select":
            if input_id == "move_down": self.action_menu.navigate((0, 1))
            elif input_id == "move_up": self.action_menu.navigate((0, -1))
            elif input_id in ("enter", "space"): self.action_menu.confirm()
                
        # Modo 3: Selección de objetivo para curación individual[cite: 4]
        elif self.mode == "target_select":
            if input_id == "move_down": self.target_menu.navigate((0, 1))
            elif input_id == "move_up": self.target_menu.navigate((0, -1))
            elif input_id in ("enter", "space"): self.target_menu.confirm()