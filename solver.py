import heapq
from collections import deque
from typing import List, Optional, Set, Tuple

from gametypes import GameState, heuristic


def find_path(start: Tuple[int, int], end: Tuple[int, int], obstacles: Set[Tuple[int, int]], width: int, height: int) -> Optional[List[str]]:
    # finds the shortest path between two points using a-star search algorithm
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


def find_longest_path(start: Tuple[int, int], obstacles: Set[Tuple[int, int]], width: int, height: int) -> Optional[List[str]]:
    # finds the longest path from a given point to any reachable cell
    longest_path = []
    q = deque([(start, [])])
    visited = {start}

    while q:
        current, path = q.popleft()

        # Check if this path is a dead end
        is_dead_end = True
        for dx, dy, direction in [(0, 1, "KEY_DOWN"), (0, -1, "KEY_UP"), (1, 0, "KEY_RIGHT"), (-1, 0, "KEY_LEFT")]:
            nx, ny = current[0] + dx, current[1] + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and (nx, ny) not in obstacles and (nx, ny) not in visited:
                is_dead_end = False
                break

        if is_dead_end and len(path) > len(longest_path):
            longest_path = path

        for dx, dy, direction in [(0, 1, "KEY_DOWN"), (0, -1, "KEY_UP"), (1, 0, "KEY_RIGHT"), (-1, 0, "KEY_LEFT")]:
            nx, ny = current[0] + dx, current[1] + dy
            if 1 <= nx < width - 1 and 1 <= ny < height - 1 and (nx, ny) not in obstacles and (nx, ny) not in visited:
                visited.add((nx, ny))
                new_path = path + [direction]
                q.append(((nx, ny), new_path))

    return longest_path


def get_next_direction(game: GameState) -> Optional[str]:
    obstacles = set(game.snake)
    path_to_fruit = find_path(game.snake[0], game.fruit, obstacles, game.term_width, game.term_height)

    if path_to_fruit:
        # simulate the snake moving to the fruit to check for traps
        virtual_snake_body = list(game.snake)
        for move in path_to_fruit:
            head_x, head_y = virtual_snake_body[0]
            if move == "KEY_LEFT":
                head_x -= 1
            elif move == "KEY_RIGHT":
                head_x += 1
            elif move == "KEY_UP":
                head_y -= 1
            elif move == "KEY_DOWN":
                head_y += 1
            virtual_snake_body.insert(0, (head_x, head_y))
            if virtual_snake_body[0] != game.fruit:
                virtual_snake_body.pop()

        # if the snake can find a path to its tail after eating the fruit, the path is safe
        if len(virtual_snake_body) > 1:
            path_to_tail = find_path(virtual_snake_body[0], virtual_snake_body[-1], set(virtual_snake_body), game.term_width, game.term_height)
            if path_to_tail:
                return path_to_fruit[0]

    # survival mode: find path to tail
    if len(game.snake) > 1:
        path_to_tail = find_path(game.snake[0], game.snake[-1], set(game.snake[:-1]), game.term_width, game.term_height)
        if path_to_tail:
            return path_to_tail[0]

    # last resort: find the longest path
    path_to_longest = find_longest_path(game.snake[0], obstacles, game.term_width, game.term_height)
    if path_to_longest:
        return path_to_longest[0]

    return None
