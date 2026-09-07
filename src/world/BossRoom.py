from gale.timer import Timer

from src.definitions.entity import ENTITY_DEFS
from src.states.entity.EntityIdleState import EntityIdleState
from src.states.entity.EntityWalkState import EntityWalkState
from src.world.Room import Room
from src.world.Doorway import Doorway
from src.Boss import Boss
import settings

class BossRoom(Room):
    def __init__(self, player, on_game_over, on_victory, entrance_direction: str):
        # Llamamos al constructor de la habitación normal
        super().__init__(player, on_game_over, on_victory)
        self.on_victory = on_victory
        self.on_game_over = on_game_over
        
        # 1. Limpiamos todas las puertas por defecto
        self.doorways = []
        
        # 2. Creamos ÚNICAMENTE la puerta por la que entramos (abierta para poder salir si queremos, o cerrada si es una trampa)
        self.doorways.append(Doorway(entrance_direction, True, self))
        self._doorways_by_direction = {
            doorway.direction: doorway for doorway in self.doorways
        }
        
        # 3. Aquí instanciaremos al Jefe en el lado opuesto a la entrada
        self._spawn_boss(entrance_direction)

    def _generate_entities(self) -> None:
        # Sobrescribimos con un pass: Ninguna criatura común aparecerá
        pass

    def _generate_objects(self) -> None:
        # Sobrescribimos con un pass: Sin vasijas, cofres ni interruptores
        pass

    def update(self, dt: float) -> None:
        flechas_vivas = [p for p in self.projectiles if p.__class__.__name__ == "Arrow"]

        super().update(dt) 

        for flecha in flechas_vivas:
            if flecha.dead and not self.boss.dead and flecha.collides(self.boss):
                self.boss.take_arrow_hit()
                print("¡Impacto atrapado en el acto!")

        if hasattr(self, 'boss') and not self.boss.dead:
            self.boss.update(dt, self.player, self)

            if self.player.collides(self.boss) and not self.player.invulnerable:
                self.player.damage(2)
                self.player.go_invulnerable(1.5)

        if self.boss.health <= 0 and not self.boss.dead:
            self.boss.dead = True
            Timer.clear()
            self.on_victory()

        for projectile in list(self.projectiles):
            if projectile.__class__.__name__ != "Arrow" and not projectile.dead:
                if projectile.collides(self.player) and not self.player.invulnerable:
                    self.player.health = 0
                    projectile.dead = True
                    self.player.dead = True
                    self.on_game_over()



    def _spawn_boss(self, entrance_direction: str) -> None:
        # Iniciamos con coordenadas centrales por defecto
        boss_x = settings.VIRTUAL_WIDTH // 2
        boss_y = settings.VIRTUAL_HEIGHT // 2
        
        # Lo alejamos hacia la pared opuesta a la entrada
        margin = settings.TILE_SIZE * 4
        
        if entrance_direction == "left":
            boss_x = settings.VIRTUAL_WIDTH - margin - 16 # (32 = ancho del jefe)
        elif entrance_direction == "right":
            boss_x = settings.MAP_RENDER_OFFSET_X + margin
        elif entrance_direction == "top":
            boss_y = settings.VIRTUAL_HEIGHT - margin - 16
        elif entrance_direction == "bottom":
            boss_y = settings.MAP_RENDER_OFFSET_Y + margin
            
        # Instanciamos al Jefe
        definition = ENTITY_DEFS["boss"]
        self.boss = Boss(
            x=boss_x,
            y=boss_y,
            width=16,
            height=16,
            walk_speed=0,
            health=2,  
            animation_defs=definition["animations"],
            states={} 
        )

        self.boss.state_machine.states = {
            "walk": lambda sm, e=self.boss: EntityWalkState(e, sm),
            "idle": lambda sm, e=self.boss: EntityIdleState(e, sm),
        }
        self.boss.change_state("idle")
        
        # Lo añadimos a la lista de entidades de la habitación para que el render/update lo procese
        self.entities.append(self.boss)