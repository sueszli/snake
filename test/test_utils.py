# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "pytest>=8.0.0",
# ]
# ///
from state import GameState
from utils import a_star_search, count_reachable_cells, dist


def test_dist():
    assert dist((0, 0), (0, 0)) == 0
    assert dist((0, 0), (3, 4)) == 7
    assert dist((5, 5), (2, 1)) == 7
    assert dist((1, 1), (1, 5)) == 4


def test_a_star_basic_path():
    game = GameState(snake=((2, 2),), fruit=(4, 4), direction="KEY_RIGHT", score=0, term_width=7, term_height=7)

    path = a_star_search(game, (2, 2), (4, 4))
    assert path is not None
    assert path[0] == (2, 2)
    assert path[-1] == (4, 4)
    assert len(path) == 5


def test_a_star_with_obstacle():
    snake = ((2, 2), (3, 2), (4, 2), (4, 3))

    game = GameState(snake=snake, fruit=(5, 2), direction="KEY_RIGHT", score=3, term_width=8, term_height=8)

    path = a_star_search(game, (2, 2), (5, 2))
    assert path is not None
    assert path[0] == (2, 2)
    assert path[-1] == (5, 2)

    for pos in path[1:]:
        assert pos not in snake or pos == snake[-1]


def test_a_star_no_path():
    snake = ((1, 1), (1, 2), (1, 3), (2, 3), (3, 3), (4, 3), (5, 3), (5, 2), (5, 1), (4, 1), (3, 1), (2, 1), (2, 2))

    game = GameState(snake=snake, fruit=(3, 2), direction="KEY_DOWN", score=12, term_width=8, term_height=8)

    path = a_star_search(game, (1, 1), (3, 2))
    assert path is None


def test_a_star_to_tail():
    snake = ((1, 1), (2, 1), (3, 1))

    game = GameState(snake=snake, fruit=(5, 5), direction="KEY_RIGHT", score=2, term_width=8, term_height=8)

    path = a_star_search(game, (1, 1), (3, 1))
    assert path is not None


def test_a_star_same_position():
    game = GameState(snake=((3, 3),), fruit=(5, 5), direction="KEY_RIGHT", score=0, term_width=8, term_height=8)

    path = a_star_search(game, (3, 3), (3, 3))
    assert path is not None
    assert len(path) == 1
    assert path[0] == (3, 3)


def test_count_reachable_cells_empty():
    game = GameState(snake=((3, 3),), fruit=(5, 5), direction="KEY_RIGHT", score=0, term_width=7, term_height=7)

    count = count_reachable_cells(game, (3, 3))
    assert count == 25


def test_count_reachable_cells_with_snake():
    snake = ((3, 1), (3, 2), (3, 3), (3, 4), (3, 5))

    game = GameState(snake=snake, fruit=(5, 5), direction="KEY_DOWN", score=4, term_width=7, term_height=7)

    count_left = count_reachable_cells(game, (1, 1))
    count_right = count_reachable_cells(game, (5, 5))

    assert count_left < 25
    assert count_right < 25
    assert count_left + count_right == 25 - len(snake)


def test_a_star_corner_to_corner():
    game = GameState(snake=((1, 1),), fruit=(5, 5), direction="KEY_RIGHT", score=0, term_width=7, term_height=7)

    path = a_star_search(game, (1, 1), (5, 5))
    assert path is not None
    assert len(path) == 9
