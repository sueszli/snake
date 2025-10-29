from functools import lru_cache
from typing import Dict, Optional, Sequence, Tuple

from state import GameState
from utils import a_star_search, count_reachable_cells

DIRECTION_VECTORS: Dict[str, Tuple[int, int]] = {
    "KEY_UP": (0, -1),
    "KEY_DOWN": (0, 1),
    "KEY_LEFT": (-1, 0),
    "KEY_RIGHT": (1, 0),
}


def _vector_to_direction(vector: Tuple[int, int]) -> Optional[str]:
    for direction, offset in DIRECTION_VECTORS.items():
        if offset == vector:
            return direction
    return None


def _within_bounds(game: GameState, position: Tuple[int, int]) -> bool:
    width = game.term_width - 2
    height = game.term_height - 2
    return 1 <= position[0] <= width and 1 <= position[1] <= height


def _is_move_valid(game: GameState, direction: str) -> bool:
    dx, dy = DIRECTION_VECTORS[direction]
    head_x, head_y = game.snake[0]
    next_head = (head_x + dx, head_y + dy)

    if not _within_bounds(game, next_head):
        return False

    if next_head in game.snake:
        return False

    return True


def _apply_move(game: GameState, direction: str) -> Optional[GameState]:
    if not _is_move_valid(game, direction):
        return None

    dx, dy = DIRECTION_VECTORS[direction]
    head_x, head_y = game.snake[0]
    next_head = (head_x + dx, head_y + dy)
    snake = list(game.snake)

    if next_head == game.fruit:
        snake.insert(0, next_head)
        score = game.score + 1
    else:
        snake.insert(0, next_head)
        snake.pop()
        score = game.score

    return GameState(
        snake=tuple(snake),
        fruit=game.fruit,
        direction=direction,
        score=score,
        term_width=game.term_width,
        term_height=game.term_height,
    )


def _direction_from_path(path: Tuple[Tuple[int, int], ...]) -> Optional[str]:
    if len(path) < 2:
        return None
    dx = path[1][0] - path[0][0]
    dy = path[1][1] - path[0][1]
    return _vector_to_direction((dx, dy))


def _has_escape_route(game: GameState) -> bool:
    # return True if the snake can keep moving safely from the given state

    # ensure that the snake will still be able to reach its tail after the move.
    path_to_tail = a_star_search(game, game.snake[0], game.snake[-1])
    if path_to_tail is not None:
        return True

    # fall back to checking the size of the accessible region to avoid dead ends.
    reachable = count_reachable_cells(game, game.snake[0])
    return reachable > 0


def _simulate_path(game: GameState, path: Sequence[Tuple[int, int]]) -> Optional[GameState]:
    state = game
    for index in range(1, len(path)):
        prev = path[index - 1]
        curr = path[index]
        direction = _vector_to_direction((curr[0] - prev[0], curr[1] - prev[1]))
        if direction is None:
            return None
        state = _apply_move(state, direction)
        if state is None:
            return None

    if state and _has_escape_route(state) and _follows_cycle(state):
        return state
    return None


def _is_path_safe(game: GameState, path: Sequence[Tuple[int, int]]) -> bool:
    if len(path) < 2:
        return False

    final_state = _simulate_path(game, path)
    return final_state is not None


def _follows_cycle(game: GameState) -> bool:
    width = game.term_width - 2
    height = game.term_height - 2
    for idx in range(len(game.snake) - 1):
        current = game.snake[idx]
        nxt = game.snake[idx + 1]
        if _hamilton_successor_map(width, height).get(nxt) != current:
            return False
    return True


OPPOSITE_DIRECTIONS = {
    "KEY_LEFT": "KEY_RIGHT",
    "KEY_RIGHT": "KEY_LEFT",
    "KEY_UP": "KEY_DOWN",
    "KEY_DOWN": "KEY_UP",
}


def _hamilton_rule(x: int, y: int, direction: str, width: int, height: int) -> str:
    if y == 1:
        target_direction = "KEY_LEFT" if x > 1 else "KEY_DOWN"
    elif x == width:
        target_direction = "KEY_UP" if y > 1 else "KEY_LEFT"
    elif y == height:
        target_direction = "KEY_RIGHT" if x % 2 != 0 else "KEY_UP"
    elif x % 2 != 0:
        target_direction = "KEY_DOWN"
    elif y > 2:
        target_direction = "KEY_UP"
    else:
        target_direction = "KEY_RIGHT"

    if OPPOSITE_DIRECTIONS[direction] == target_direction:
        return "KEY_DOWN" if y + 1 <= height else "KEY_UP"
    return target_direction


@lru_cache(maxsize=None)
def _hamilton_successor_map(width: int, height: int) -> Dict[Tuple[int, int], Tuple[int, int]]:
    assert width % 2 == 0, "width must be even for this Hamiltonian cycle."

    successors: Dict[Tuple[int, int], Tuple[int, int]] = {}
    x, y = width, 1
    direction = "KEY_LEFT"

    start = (x, y)
    while True:
        move = _hamilton_rule(x, y, direction, width, height)
        dx, dy = DIRECTION_VECTORS[move]
        nx, ny = x + dx, y + dy
        successors[(x, y)] = (nx, ny)
        x, y = nx, ny
        direction = move
        if (x, y) == start:
            break

    return successors


def _hamilton_direction(game: GameState) -> Optional[str]:
    width = game.term_width - 2
    height = game.term_height - 2
    head = game.snake[0]
    successor_map = _hamilton_successor_map(width, height)
    next_cell = successor_map.get(head)
    if next_cell is None:
        return None

    dx = next_cell[0] - head[0]
    dy = next_cell[1] - head[1]
    return _vector_to_direction((dx, dy))


def get_next_direction(game: GameState) -> Optional[str]:
    head = game.snake[0]

    path_to_fruit = a_star_search(game, head, game.fruit)
    if path_to_fruit and len(path_to_fruit) > 1:
        direction = _direction_from_path(tuple(path_to_fruit))
        if direction and _is_move_valid(game, direction) and _is_path_safe(game, path_to_fruit):
            return direction

    return _hamilton_direction(game)
