# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "blessed==1.20.0",
# ]
# ///
import argparse
import random
import sys
import time
from typing import Optional

import blessed

from gametypes import GameState
from solver import get_next_direction


def update_game_state(game: GameState) -> Optional[GameState]:
    direction = get_next_direction(game)
    if direction is None:
        return None

    head_x, head_y = game.snake[0]
    if direction == "KEY_LEFT":
        head_x -= 1
    elif direction == "KEY_RIGHT":
        head_x += 1
    elif direction == "KEY_UP":
        head_y -= 1
    elif direction == "KEY_DOWN":
        head_y += 1
    new_head = (head_x, head_y)

    if new_head in game.snake or not (1 <= new_head[0] < game.term_width - 1 and 1 <= new_head[1] < game.term_height - 1):
        return None

    new_snake = list(game.snake)
    new_snake.insert(0, new_head)

    if new_head == game.fruit:
        new_score = game.score + 1
        all_cells = set((x, y) for x in range(1, game.term_width - 1) for y in range(1, game.term_height - 1))
        valid_fruit_cells = all_cells - set(new_snake)
        if not valid_fruit_cells:
            return GameState(tuple(new_snake), new_head, direction, new_score, game.term_width, game.term_height)
        new_fruit = random.choice(list(valid_fruit_cells))

        return GameState(tuple(new_snake), new_fruit, direction, new_score, game.term_width, game.term_height)
    else:
        new_snake.pop()
        return GameState(tuple(new_snake), game.fruit, direction, game.score, game.term_width, game.term_height)


def render(term: blessed.Terminal, game: GameState):
    print(term.home + term.clear, end="")

    print(term.move_xy(0, 0) + "┌" + "─" * (game.term_width - 2) + "┐")
    for y in range(1, game.term_height - 1):
        print(term.move_xy(0, y) + "│", end="")
        print(term.move_xy(game.term_width - 1, y) + "│")
    print(term.move_xy(0, game.term_height - 1) + "└" + "─" * (game.term_width - 2) + "┘", end="")

    score_text = f"Score: {game.score}"
    print(term.move_xy(1, 0) + score_text, end="")

    for x, y in game.snake:
        print(term.move_xy(x, y) + "█", end="")

    print(term.move_xy(game.fruit[0], game.fruit[1]) + "ó", end="")
    sys.stdout.flush()


def game_loop(term: blessed.Terminal, initial_game_state: GameState):
    game = initial_game_state
    last_game_state = initial_game_state
    with term.cbreak(), term.hidden_cursor():
        while game:
            render(term, game)
            last_game_state = game
            game = update_game_state(game)
            time.sleep(0.01)
    return last_game_state


def cli_game_loop(initial_game_state: GameState):
    game = initial_game_state
    last_game_state = initial_game_state
    steps_since_last_fruit = 0

    while game:
        last_game_state = game
        prev_score = game.score
        game = update_game_state(game)

        if not game:
            break

        if game.score > prev_score:
            steps_since_last_fruit = 0
        else:
            steps_since_last_fruit += 1

        live_lock = steps_since_last_fruit > (initial_game_state.term_width - 2) * (initial_game_state.term_height - 2) * 2
        if live_lock:
            break
    return last_game_state


def main():
    parser = argparse.ArgumentParser(description="run the snake game.")
    parser.add_argument("--cli", action="store_true", help="run in CLI mode without graphics.")
    parser.add_argument("--runs", type=int, default=1, help="number of times to run the game.")
    args = parser.parse_args()

    if args.cli:
        total_score = 0
        for _ in range(args.runs):
            term_width = 50
            term_height = 20
            snake = tuple((term_width // 2 - i, term_height // 2) for i in range(3))
            all_cells = set((x, y) for x in range(1, term_width - 1) for y in range(1, term_height - 1))
            valid_fruit_cells = all_cells - set(snake)
            fruit = random.choice(list(valid_fruit_cells))
            initial_game_state = GameState(snake=snake, fruit=fruit, direction="KEY_RIGHT", score=0, term_width=term_width, term_height=term_height)
            final_game_state = cli_game_loop(initial_game_state)
            total_score += final_game_state.score
            max_size = (term_width - 2) * (term_height - 2)
        print(f"Average score: {total_score / args.runs}")
        exit(0)

    term = blessed.Terminal()
    snake = tuple((term.width // 2 - i, term.height // 2) for i in range(3))
    all_cells = set((x, y) for x in range(1, term.width - 1) for y in range(1, term.height - 1))
    valid_fruit_cells = all_cells - set(snake)
    fruit = random.choice(list(valid_fruit_cells))
    initial_game_state = GameState(snake=snake, fruit=fruit, direction="KEY_RIGHT", score=0, term_width=term.width, term_height=term.height)
    final_game_state = game_loop(term, initial_game_state)
    print(term.home + term.clear)
    score = final_game_state.score
    max_size = (final_game_state.term_width - 2) * (final_game_state.term_height - 2)
    if len(final_game_state.snake) >= max_size:
        msg = "You won!"
    else:
        msg = f"Game Over! Score: {score}"
    print(term.move_xy(term.width // 2 - len(msg) // 2, term.height // 2) + msg)


if __name__ == "__main__":
    main()
