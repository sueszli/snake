from typing import Optional

from gametypes import GameState
from pathfinding import a_star_search, count_reachable_cells


def get_next_direction(game: GameState) -> Optional[str]:
    """
    a solver that uses a* to find the shortest path to the fruit,
    with a fallback to a hamiltonian cycle to avoid getting trapped.
    """
    head = game.snake[0]
    fruit = game.fruit

    # 1. a* search for the shortest path to the fruit
    path_to_fruit = a_star_search(game, head, fruit)

    if path_to_fruit and len(path_to_fruit) > 1:
        # 2. safety check: after eating the fruit, is the board partitioned?
        # create a temporary game state to simulate the move
        temp_snake = list(game.snake)
        temp_snake.insert(0, path_to_fruit[1])
        if path_to_fruit[1] == fruit:  # it will eat the fruit
            pass  # the tail is not removed
        else:
            temp_snake.pop()

        temp_game_state = GameState(
            snake=tuple(temp_snake),
            fruit=game.fruit,
            direction=game.direction,  # this is not used by a*
            score=game.score,
            term_width=game.term_width,
            term_height=game.term_height,
        )

        # count total empty cells
        total_empty_cells = (game.term_width - 2) * (game.term_height - 2) - len(temp_game_state.snake)

        # count cells reachable from the new head
        reachable_cells = count_reachable_cells(temp_game_state, temp_game_state.snake[0])

        if reachable_cells >= len(temp_game_state.snake):
            # if the move is safe, take the step
            next_move = path_to_fruit[1]
            if next_move[0] > head[0]:
                return "KEY_RIGHT"
            elif next_move[0] < head[0]:
                return "KEY_LEFT"
            elif next_move[1] > head[1]:
                return "KEY_DOWN"
            elif next_move[1] < head[1]:
                return "KEY_UP"

    # 3. fallback to hamiltonian cycle if no safe path to fruit is found
    return hamiltonian_cycle(game)


def hamiltonian_cycle(game: GameState) -> Optional[str]:
    """
    a solver that follows a pre-defined hamiltonian cycle on the grid.
    this ensures the snake covers all cells without collision, running
    perpetually until it fills the entire board.
    the algorithm is designed for a grid with an even width.
    """
    head_x, head_y = game.snake[0]
    direction = game.direction
    width = game.term_width - 2
    height = game.term_height - 2

    # this algorithm for a hamiltonian cycle requires the grid width to be even.
    if width % 2 != 0:
        # fallback for odd width grids. a different algorithm would be needed.
        return "KEY_RIGHT"

    # determine the target direction based on the hamiltonian cycle path.
    target_direction = None
    if head_y == 1:
        if head_x > 1:
            target_direction = "KEY_LEFT"
        else:  # at (1,1)
            target_direction = "KEY_DOWN"
    elif head_x == width:  # last column
        if head_y > 1:
            target_direction = "KEY_UP"
        else:  # at (width, 1)
            target_direction = "KEY_LEFT"
    elif head_y == height:  # bottom row
        if head_x % 2 != 0:
            target_direction = "KEY_RIGHT"
        else:
            target_direction = "KEY_UP"
    elif head_x % 2 != 0:  # odd columns
        target_direction = "KEY_DOWN"
    elif head_x % 2 == 0:  # even columns
        if head_y > 2:
            target_direction = "KEY_UP"
        else:  # at y=2
            target_direction = "KEY_RIGHT"

    # if the snake's current direction is opposite to the target direction
    # (e.g., at the start), choose an alternate move to get onto the cycle.
    if (direction == "KEY_RIGHT" and target_direction == "KEY_LEFT") or (direction == "KEY_LEFT" and target_direction == "KEY_RIGHT") or (direction == "KEY_UP" and target_direction == "KEY_DOWN") or (direction == "KEY_DOWN" and target_direction == "KEY_UP"):
        # try to move down first, then up, to join the cycle path.
        next_x, next_y = head_x, head_y + 1  # try down
        if (next_x, next_y) not in game.snake and next_y <= height:
            return "KEY_DOWN"
        else:
            return "KEY_UP"

    return target_direction
