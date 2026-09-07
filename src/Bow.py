from gale.factory import Factory

from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.GameObject import GameObject
from src.Projectile import Projectile 

class Arrow(Projectile):
    def __init__(self, x: float, y: float, direction: str) -> None:
        # 1. Construimos el objeto visual (hitbox y textura)
        arrow_obj = GameObject(GAME_OBJECT_DEFS["arrows"], x, y)

        if direction in arrow_obj.states:
            arrow_obj.state = direction
        
        # 2. Inicializamos la clase padre (Projectile) pasándole el objeto y la dirección
        super().__init__(arrow_obj, direction)

class Bow:
    def __init__(self) -> None:
        # La fábrica se encargará de instanciar proyectiles por nosotros
        self.arrow_factory = Factory(Arrow)

    def fire(self, x: float, y: float, direction: str):
        # Invocamos la creación sin usar Projectile(...) directamente
        return self.arrow_factory.create(x, y, {"direction": direction})