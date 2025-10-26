from typing import Optional

from gametypes import GameState


def get_next_direction(game: GameState) -> Optional[str]:
    """
    A solver that follows a pre-defined Hamiltonian cycle on the grid.
    This ensures the snake covers all cells without collision, running
    perpetually until it fills the entire board.
    The algorithm is designed for a grid with an even width.
    """
    head_x, head_y = game.snake[0]
    direction = game.direction
    width = game.term_width - 2
    height = game.term_height - 2

    # This algorithm for a Hamiltonian cycle requires the grid width to be even.
    if width % 2 != 0:
        # Fallback for odd width grids. A different algorithm would be needed.
        return "KEY_RIGHT"

    # Determine the target direction based on the Hamiltonian cycle path.
    target_direction = None
    if head_y == 1:
        if head_x > 1:
            target_direction = "KEY_LEFT"
        else:  # at (1,1)
            target_direction = "KEY_DOWN"
    elif head_x == width:  # Last column
        if head_y > 1:
            target_direction = "KEY_UP"
        else:  # at (width, 1)
            target_direction = "KEY_LEFT"
    elif head_y == height:  # Bottom row
        if head_x % 2 != 0:
            target_direction = "KEY_RIGHT"
        else:
            target_direction = "KEY_UP"
    elif head_x % 2 != 0:  # Odd columns
        target_direction = "KEY_DOWN"
    elif head_x % 2 == 0:  # Even columns
        if head_y > 2:
            target_direction = "KEY_UP"
        else:  # at y=2
            target_direction = "KEY_RIGHT"

    # If the snake's current direction is opposite to the target direction
    # (e.g., at the start), choose an alternate move to get onto the cycle.
    if (direction == "KEY_RIGHT" and target_direction == "KEY_LEFT") or (direction == "KEY_LEFT" and target_direction == "KEY_RIGHT") or (direction == "KEY_UP" and target_direction == "KEY_DOWN") or (direction == "KEY_DOWN" and target_direction == "KEY_UP"):
        # Try to move down first, then up, to join the cycle path.
        next_x, next_y = head_x, head_y + 1  # Try down
        if (next_x, next_y) not in game.snake and next_y <= height:
            return "KEY_DOWN"
        else:
            return "KEY_UP"

    return target_direction
