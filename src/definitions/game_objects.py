"""
ISPPV1 2023
Study Case: The Legend of the Princess (ARPG)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition for game objects.
"""

from typing import Any, Dict

import settings


def _pickup_heart(player, obj) -> None:
    player.heal(2)
    settings.SOUNDS["heart-taken"].play()

def _open_chest(player, obj) -> None:
    print(f"Estado del cofre antes: {obj.state}") # Para depurar
    if obj.state == "closed":
        obj.state = "open"  # Esto obliga a GameObject.render a usar el frame del estado "open"
        obj.interactable = False
        player.hasBow = True
        print("¡Arco obtenido y cofre abierto!")

        # settings.SOUNDS["chest_open"].play()

GAME_OBJECT_DEFS: Dict[str, Dict[str, Any]] = {
    "switch": {
        "type": "switch",
        "texture": "switches",
        "frame": 2,
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "unpressed",
        "states": {
            "unpressed": {"frame": 2},
            "pressed": {"frame": 1},
        },
    },
    "pot": {
        "type": "pot",
        "texture": "tiles",
        "frame": 16,
        "width": 16,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "default",
        "takeable": True,
        "states": {
            "default": {"frame": 16},
        },
    },
    # Definition of heart as a consumable object type.
    "heart": {
        "type": "heart",
        "texture": "hearts",
        "frame": 5,
        "width": 16,
        "height": 16,
        "solid": False,
        "consumable": True,
        "default_state": "default",
        "states": {
            "default": {"frame": 5},
        },
        "on_consume": _pickup_heart,
    },
    "chest": {
        "type": "chest",
        "texture": "tiles",
        "frame": 167,
        "width": 16,
        "height": 16,
        "solid": True,
        "consumable": False,
        "default_state": "closed",
        "takeable": False,
        "interactable": True,
        "states": {
            "closed": {"frame": 167},
            "open": {"frame": 128},
        },
        "on_interact": _open_chest,
    },
    "arrows": {
        "type": "projectile",
        "texture": "arrows",
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "right",
        "states": {
            "right": {"frame": 1},
            "up": {"frame": 2},
            "left": {"frame": 3},
            "down": {"frame": 4},
        }
    },
    "fireball": {
        "type": "projectile",
        "texture": "fireball",
        "width": 16,
        "height": 16,
        "solid": False,
        "default_state": "right",
        "states": {
            "right": {"frame": 1},
            "up": {"frame": 2},
            "left": {"frame": 3},
            "down": {"frame": 4},
        }
    },
}
