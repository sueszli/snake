import heapq
from typing import List, Optional, Tuple

from gametypes import GameState


def heuristic(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Calculates the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def a_star_search(game: GameState, start: Tuple[int, int], goal: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
    """
    A* search algorithm to find the shortest path from start to goal.
    """
    width = game.term_width - 2
    height = game.term_height - 2

    # The set of nodes already evaluated
    closed_set = set()

    # The set of currently discovered nodes that are not evaluated yet.
    # Initially, only the start node is known.
    open_set = [(0, start)]  # (f_score, node)

    # For each node, which node it can most efficiently be reached from.
    # If a node can be reached from many nodes, came_from will eventually contain the
    # most efficient previous step.
    came_from = {}

    # For each node, the cost of getting from the start node to that node.
    g_score = {(x, y): float("inf") for x in range(1, width + 1) for y in range(1, height + 1)}
    g_score[start] = 0

    # For each node, the total cost of getting from the start node to the goal
    # by passing by that node. That value is partly known, partly heuristic.
    f_score = {(x, y): float("inf") for x in range(1, width + 1) for y in range(1, height + 1)}
    f_score[start] = heuristic(start, goal)

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        closed_set.add(current)

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)

            if not (1 <= neighbor[0] <= width and 1 <= neighbor[1] <= height):
                continue

            if neighbor in closed_set:
                continue

            # Don't run into the snake's body
            # We allow the path to go to the tail, because it will move
            if neighbor in game.snake and neighbor != game.snake[-1]:
                continue

            tentative_g_score = g_score[current] + 1

            if tentative_g_score < g_score.get(neighbor, float("inf")):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, goal)
                if (f_score[neighbor], neighbor) not in open_set:
                    heapq.heappush(open_set, (f_score[neighbor], neighbor))

    return None


def count_reachable_cells(game: GameState, start: Tuple[int, int]) -> int:
    """
    Counts the number of reachable cells from a starting point using BFS.
    """
    width = game.term_width - 2
    height = game.term_height - 2
    q = [start]
    visited = {start}
    count = 0
    while q:
        cell = q.pop(0)
        count += 1
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (cell[0] + dx, cell[1] + dy)

            if not (1 <= neighbor[0] <= width and 1 <= neighbor[1] <= height):
                continue

            if neighbor in visited:
                continue

            if neighbor in game.snake:
                continue

            visited.add(neighbor)
            q.append(neighbor)
    return count
