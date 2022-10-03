from jchess.game.state import GameState as GameState
from jchess.geometry import Vector as Vector
from jchess.pieces import Piece as Piece, Player as Player, Role as Role

def targets_of_(game: GameState, attacker: Piece) -> list[Vector]: ...
