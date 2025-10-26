# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "blessed==1.20.0",
# ]
# ///
import random
import sys
import time
import heapq

import blessed


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def find_path(start, end, obstacles, width, height):
    neighbors = [(0, 1, "KEY_DOWN"), (0, -1, "KEY_UP"), (1, 0, "KEY_RIGHT"), (-1, 0, "KEY_LEFT")]
    close_set = set()
    came_from = {}
    gscore = {start: 0}
    fscore = {start: heuristic(start, end)}
    oheap = []

    heapq.heappush(oheap, (fscore[start], start))

    while oheap:
        current = heapq.heappop(oheap)[1]

        if current == end:
            data = []
            while current in came_from:
                prev, direction = came_from[current]
                data.append(direction)
                current = prev
            return data[::-1]

        close_set.add(current)
        for i, j, direction in neighbors:
            neighbor = current[0] + i, current[1] + j
            if not (1 <= neighbor[0] < width - 1 and 1 <= neighbor[1] < height - 1):
                continue
            if neighbor in obstacles and neighbor != end:
                continue

            tentative_g_score = gscore[current] + 1
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue

            if tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1] for i in oheap]:
                came_from[neighbor] = (current, direction)
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, end)
                heapq.heappush(oheap, (fscore[neighbor], neighbor))

    return None


def update_state(game, term):
    new_head = move_snake(game)

    # Game over conditions
    body = game["snake"][1:]
    has_collision_with_self = new_head in body
    has_collision_with_wall = not (1 <= new_head[0] < term.width - 1 and 1 <= new_head[1] < term.height - 1)
    if has_collision_with_self or has_collision_with_wall:
        return None  # Signal game over

    game["snake"].insert(0, new_head)

    handle_fruit_eating(game, term)

    return game


def move_snake(game):
    head_x, head_y = game["snake"][0]
    if game["direction"] == "KEY_LEFT":
        head_x -= 1
    elif game["direction"] == "KEY_RIGHT":
        head_x += 1
    elif game["direction"] == "KEY_UP":
        head_y -= 1
    elif game["direction"] == "KEY_DOWN":
        head_y += 1
    return (head_x, head_y)


def handle_fruit_eating(game, term):
    if game["snake"][0] == game["fruit"]:
        game["score"] += 1
        game["fruit"] = (random.randint(1, term.width - 2), random.randint(1, term.height - 2))
    else:
        game["snake"].pop()


def render(term, game):
    print(term.home + term.clear, end="")

    # Draw border
    print(term.move_xy(0, 0) + "┌" + "─" * (term.width - 2) + "┐")
    for y in range(1, term.height - 1):
        print(term.move_xy(0, y) + "│", end="")
        print(term.move_xy(term.width - 1, y) + "│")
    print(term.move_xy(0, term.height - 1) + "└" + "─" * (term.width - 2) + "┘", end="")

    # snake
    for x, y in game["snake"]:
        print(term.move_xy(x, y) + "█", end="")

    # fruit
    print(term.move_xy(game["fruit"][0], game["fruit"][1]) + "ó", end="")
    sys.stdout.flush()


def game_loop(term, game):
    path = []
    with term.cbreak(), term.hidden_cursor():
        while True:
            if not path:
                obstacles = set(game["snake"])
                path = find_path(game["snake"][0], game["fruit"], obstacles, term.width, term.height)
                if not path:
                    # No path to fruit, just try to survive
                    # A simple survival strategy: keep moving in the current direction,
                    # and turn if there is an obstacle.
                    # This is a very basic strategy and might not be optimal.
                    head = game["snake"][0]
                    x, y = head
                    direction = game["direction"]
                    
                    # Check if the next move is an obstacle
                    next_x, next_y = x, y
                    if direction == "KEY_LEFT": next_x -= 1
                    elif direction == "KEY_RIGHT": next_x += 1
                    elif direction == "KEY_UP": next_y -= 1
                    elif direction == "KEY_DOWN": next_y += 1

                    if (next_x, next_y) in obstacles or not (1 <= next_x < term.width - 1 and 1 <= next_y < term.height - 1):
                        # Try to find a valid move
                        for new_direction in ["KEY_UP", "KEY_DOWN", "KEY_LEFT", "KEY_RIGHT"]:
                            game["direction"] = new_direction
                            next_x, next_y = x, y
                            if new_direction == "KEY_LEFT": next_x -= 1
                            elif new_direction == "KEY_RIGHT": next_x += 1
                            elif new_direction == "KEY_UP": next_y -= 1
                            elif new_direction == "KEY_DOWN": next_y += 1
                            
                            if (next_x, next_y) not in obstacles and (1 <= next_x < term.width - 1 and 1 <= next_y < term.height - 1):
                                break
                        else:
                            # No valid move, game over
                            return game
                    
                    path = [game["direction"]]


            if path:
                game["direction"] = path.pop(0)

            # update state
            game = update_state(game, term)
            if game is None:
                break

            # render
            render(term, game)

            time.sleep(0.01)  # game speed

    return game


def main():
    term = blessed.Terminal()
    game = {
        "snake": [(term.width // 2 - i, term.height // 2) for i in range(3)],
        "fruit": (random.randint(1, term.width - 2), random.randint(1, term.height - 2)),
        "direction": "KEY_RIGHT",
        "score": 0,
    }

    final_game_state = game_loop(term, game)

    # "game over" screen
    print(term.home + term.clear)
    score = final_game_state["score"] if final_game_state else game["score"]
    msg = f"Game Over! Score: {score}"
    print(term.move_xy(term.width // 2 - len(msg) // 2, term.height // 2) + msg)


if __name__ == "__main__":
    main()