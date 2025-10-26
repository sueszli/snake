from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class GameState:
    snake: Tuple[Tuple[int, int], ...]
    fruit: Tuple[Tuple[int, int]]
    direction: str
    score: int
    term_width: int
    term_height: int


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    # calculates the manhattan distance between two points
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
