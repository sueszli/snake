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
