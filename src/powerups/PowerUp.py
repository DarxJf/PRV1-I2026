from src.Tile import Tile

class PowerUp(Tile):
    def __init__(self, i, j, color, variety):
        super().__init__(i, j, color, variety)

    def activate(self, board) -> list:
        raise NotImplementedError("Es necesario implementar metodo activate")
