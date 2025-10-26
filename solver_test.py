# /// script
# requires-python = ">=3.10"
# ///
import unittest

from solver import find_path


class TestFindPath(unittest.TestCase):
    def test_simple_path(self):
        """Test a simple path from start to end."""
        path = find_path(start=(1, 1), end=(3, 1), obstacles=set(), width=5, height=5)
        self.assertEqual(path, ["KEY_RIGHT", "KEY_RIGHT"])

    def test_no_path(self):
        """Test a scenario where no path exists."""
        obstacles = {(2, y) for y in range(5)}
        path = find_path(start=(1, 1), end=(3, 1), obstacles=obstacles, width=5, height=5)
        self.assertIsNone(path)

    def test_start_is_end(self):
        """Test when start and end points are the same."""
        path = find_path(start=(1, 1), end=(1, 1), obstacles=set(), width=5, height=5)
        self.assertEqual(path, [])

    def test_with_obstacles(self):
        """Test a path that must navigate around obstacles."""
        obstacles = {(2, 2)}
        path = find_path(start=(1, 2), end=(3, 2), obstacles=obstacles, width=5, height=5)
        self.assertIn(
            path,
            [
                ["KEY_UP", "KEY_RIGHT", "KEY_RIGHT", "KEY_DOWN"],
                ["KEY_DOWN", "KEY_RIGHT", "KEY_RIGHT", "KEY_UP"],
            ],
        )

    def test_path_along_wall(self):
        """Test a path along the boundary walls."""
        path = find_path(start=(1, 1), end=(3, 1), obstacles=set(), width=5, height=3)
        self.assertEqual(path, ["KEY_RIGHT", "KEY_RIGHT"])

    def test_no_path_start_blocked(self):
        """Test where the start is completely blocked."""
        obstacles = {(1, 2), (2, 1), (0, 1), (1, 0)}
        path = find_path(start=(1, 1), end=(3, 3), obstacles=obstacles, width=5, height=5)
        self.assertIsNone(path)


if __name__ == "__main__":
    unittest.main()
