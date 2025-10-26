# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "blessed==1.20.0",
# ]
# ///
import random

import blessed


def update_state(game, key, term):
    # Update direction based on key press
    if key.is_sequence:
        game["direction"] = key.name

    # Move snake
    head_x, head_y = game["snake"][0]
    if game["direction"] == "KEY_LEFT":
        head_x -= 1
    elif game["direction"] == "KEY_RIGHT":
        head_x += 1
    elif game["direction"] == "KEY_UP":
        head_y -= 1
    elif game["direction"] == "KEY_DOWN":
        head_y += 1

    # Create new head
    new_head = (head_x, head_y)

    # Game over conditions
    body = game["snake"][1:]
    if new_head in body or not (0 <= new_head[0] < term.width and 0 <= new_head[1] < term.height):
        return None  # Signal game over

    game["snake"].insert(0, new_head)

    # Eat fruit
    if game["snake"][0] == game["fruit"]:
        game["score"] += 1
        game["fruit"] = (
            random.randint(0, term.width - 1),
            random.randint(0, term.height - 1),
        )
    else:
        game["snake"].pop()

    return game


def render(term, game):
    # Clear screen
    print(term.home + term.clear)

    # Draw snake
    for x, y in game["snake"]:
        print(term.move_xy(x, y) + "█")

    # Draw fruit
    print(term.move_xy(game["fruit"][0], game["fruit"][1]) + "ó")


def main():
    term = blessed.Terminal()

    game = {
        "snake": [(term.width // 2, term.height // 2)],
        "fruit": (random.randint(0, term.width - 1), random.randint(0, term.height - 1)),
        "direction": "KEY_RIGHT",
        "score": 0,
    }

    with term.cbreak(), term.hidden_cursor():
        val = ""
        while val.lower() != "q":
            render(term, game)
            val = term.inkey(timeout=0.1)  # game speed
            game = update_state(game, val, term)
            if game is None:
                break

    # "game over" screen
    print(term.home + term.clear)
    msg = f"Game Over! Score: {game['score'] if game else 0}"
    print(term.move_xy(term.width // 2 - len(msg) // 2, term.height // 2) + msg)


if __name__ == "__main__":
    main()
