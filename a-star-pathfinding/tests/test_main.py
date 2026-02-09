"""Unit tests for A* pathfinding module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import AStarPathfinder, Node


class TestNode:
    """Test cases for Node class."""

    def test_node_creation(self):
        """Test node creation."""
        node = Node(5, 10)
        assert node.x == 5
        assert node.y == 10
        assert node.g == float("inf")
        assert node.h == 0.0

    def test_node_equality(self):
        """Test node equality."""
        node1 = Node(5, 10)
        node2 = Node(5, 10)
        node3 = Node(5, 11)
        assert node1 == node2
        assert node1 != node3

    def test_node_comparison(self):
        """Test node comparison for priority queue."""
        node1 = Node(0, 0, g=5.0, h=3.0)
        node2 = Node(1, 1, g=4.0, h=4.0)
        assert node1 < node2  # f=8 < f=8, but h=3 < h=4

    def test_node_hash(self):
        """Test node hashing."""
        node1 = Node(5, 10)
        node2 = Node(5, 10)
        assert hash(node1) == hash(node2)


class TestAStarPathfinder:
    """Test cases for AStarPathfinder class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def pathfinder(self, config_file):
        """Create AStarPathfinder instance."""
        return AStarPathfinder(config_path=config_file)

    @pytest.fixture
    def simple_grid(self):
        """Create simple 5x5 grid."""
        return [[0 for _ in range(5)] for _ in range(5)]

    def test_manhattan_distance(self, pathfinder):
        """Test Manhattan distance heuristic."""
        dist = pathfinder.manhattan_distance(0, 0, 3, 4)
        assert dist == 7

    def test_euclidean_distance(self, pathfinder):
        """Test Euclidean distance heuristic."""
        dist = pathfinder.euclidean_distance(0, 0, 3, 4)
        assert abs(dist - 5.0) < 0.001

    def test_chebyshev_distance(self, pathfinder):
        """Test Chebyshev distance heuristic."""
        dist = pathfinder.chebyshev_distance(0, 0, 3, 4)
        assert dist == 4

    def test_diagonal_distance(self, pathfinder):
        """Test diagonal distance heuristic."""
        dist = pathfinder.diagonal_distance(0, 0, 3, 4)
        assert dist > 0

    def test_find_path_simple(self, pathfinder, simple_grid):
        """Test finding path in simple grid."""
        path, stats = pathfinder.find_path(
            simple_grid, (0, 0), (4, 4), "manhattan"
        )
        assert path is not None
        assert len(path) > 0
        assert path[0] == (0, 0)
        assert path[-1] == (4, 4)
        assert stats["success"] is True

    def test_find_path_with_obstacles(self, pathfinder):
        """Test finding path with obstacles."""
        grid = [[0 for _ in range(5)] for _ in range(5)]
        grid[2][0] = 1
        grid[2][1] = 1
        grid[2][2] = 1
        grid[2][3] = 1
        grid[2][4] = 1
        path, stats = pathfinder.find_path(
            grid, (0, 0), (4, 4), "manhattan"
        )
        assert path is not None
        assert stats["success"] is True

    def test_find_path_no_path(self, pathfinder):
        """Test finding path when no path exists."""
        grid = [[0 for _ in range(5)] for _ in range(5)]
        grid[2][0] = 1
        grid[2][1] = 1
        grid[2][2] = 1
        grid[2][3] = 1
        grid[2][4] = 1
        grid[1][2] = 1
        grid[3][2] = 1
        path, stats = pathfinder.find_path(
            grid, (0, 0), (4, 4), "manhattan"
        )
        assert path is None
        assert stats["success"] is False

    def test_find_path_start_equals_goal(self, pathfinder, simple_grid):
        """Test finding path when start equals goal."""
        path, stats = pathfinder.find_path(
            simple_grid, (2, 2), (2, 2), "manhattan"
        )
        assert path is not None
        assert len(path) == 1
        assert path[0] == (2, 2)

    def test_find_path_empty_grid(self, pathfinder):
        """Test finding path with empty grid."""
        with pytest.raises(ValueError, match="cannot be empty"):
            pathfinder.find_path([], (0, 0), (0, 0), "manhattan")

    def test_find_path_invalid_start(self, pathfinder, simple_grid):
        """Test finding path with invalid start position."""
        with pytest.raises(ValueError, match="out of grid bounds"):
            pathfinder.find_path(simple_grid, (10, 10), (4, 4), "manhattan")

    def test_find_path_invalid_goal(self, pathfinder, simple_grid):
        """Test finding path with invalid goal position."""
        with pytest.raises(ValueError, match="out of grid bounds"):
            pathfinder.find_path(simple_grid, (0, 0), (10, 10), "manhattan")

    def test_find_path_start_is_obstacle(self, pathfinder):
        """Test finding path when start is obstacle."""
        grid = [[0 for _ in range(5)] for _ in range(5)]
        grid[0][0] = 1
        with pytest.raises(ValueError, match="is an obstacle"):
            pathfinder.find_path(grid, (0, 0), (4, 4), "manhattan")

    def test_find_path_goal_is_obstacle(self, pathfinder):
        """Test finding path when goal is obstacle."""
        grid = [[0 for _ in range(5)] for _ in range(5)]
        grid[4][4] = 1
        with pytest.raises(ValueError, match="is an obstacle"):
            pathfinder.find_path(grid, (0, 0), (4, 4), "manhattan")

    def test_find_path_invalid_heuristic(self, pathfinder, simple_grid):
        """Test finding path with invalid heuristic."""
        with pytest.raises(ValueError, match="Unknown heuristic"):
            pathfinder.find_path(simple_grid, (0, 0), (4, 4), "invalid")

    def test_find_path_all_heuristics(self, pathfinder, simple_grid):
        """Test finding path with all heuristics."""
        heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal"]
        for heuristic in heuristics:
            path, stats = pathfinder.find_path(
                simple_grid, (0, 0), (4, 4), heuristic
            )
            assert path is not None
            assert stats["success"] is True

    def test_find_path_diagonal_movement(self, pathfinder, simple_grid):
        """Test finding path with diagonal movement."""
        path, stats = pathfinder.find_path(
            simple_grid, (0, 0), (4, 4), "manhattan", allow_diagonal=True
        )
        assert path is not None
        assert stats["success"] is True

    def test_visualize_path(self, pathfinder, simple_grid):
        """Test path visualization."""
        path, _ = pathfinder.find_path(
            simple_grid, (0, 0), (4, 4), "manhattan"
        )
        visualization = pathfinder.visualize_path(
            simple_grid, path, (0, 0), (4, 4)
        )
        assert "S" in visualization
        assert "G" in visualization
        assert "*" in visualization

    def test_visualize_path_no_path(self, pathfinder, simple_grid):
        """Test visualization when no path exists."""
        visualization = pathfinder.visualize_path(
            simple_grid, None, (0, 0), (4, 4)
        )
        assert "S" in visualization
        assert "G" in visualization

    def test_compare_heuristics(self, pathfinder, simple_grid):
        """Test comparing different heuristics."""
        comparison = pathfinder.compare_heuristics(
            simple_grid, (0, 0), (4, 4), iterations=1
        )
        assert comparison["grid_size"] == (5, 5)
        assert "manhattan" in comparison
        assert "euclidean" in comparison
        assert "chebyshev" in comparison
        assert "diagonal" in comparison

    def test_compare_heuristics_with_iterations(self, pathfinder, simple_grid):
        """Test comparison with multiple iterations."""
        comparison = pathfinder.compare_heuristics(
            simple_grid, (0, 0), (4, 4), iterations=10
        )
        assert comparison["iterations"] == 10
        assert comparison["manhattan"]["success"] is True

    def test_generate_report_success(self, pathfinder, simple_grid, temp_dir):
        """Test report generation."""
        comparison = pathfinder.compare_heuristics(
            simple_grid, (0, 0), (4, 4)
        )
        report_path = temp_dir / "report.txt"

        report = pathfinder.generate_report(
            comparison, output_path=str(report_path)
        )

        assert "A* PATHFINDING" in report
        assert "MANHATTAN" in report
        assert "EUCLIDEAN" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, pathfinder, simple_grid):
        """Test report generation without saving to file."""
        comparison = pathfinder.compare_heuristics(
            simple_grid, (0, 0), (4, 4)
        )
        report = pathfinder.generate_report(comparison)

        assert "A* PATHFINDING" in report
        assert "MANHATTAN" in report
        assert "EUCLIDEAN" in report

    def test_find_path_large_grid(self, pathfinder):
        """Test finding path in larger grid."""
        grid = [[0 for _ in range(20)] for _ in range(20)]
        path, stats = pathfinder.find_path(
            grid, (0, 0), (19, 19), "manhattan"
        )
        assert path is not None
        assert stats["success"] is True

    def test_find_path_complex_obstacles(self, pathfinder):
        """Test finding path with complex obstacle pattern."""
        grid = [[0 for _ in range(10)] for _ in range(10)]
        for i in range(1, 9):
            grid[i][5] = 1
        path, stats = pathfinder.find_path(
            grid, (0, 0), (9, 9), "manhattan"
        )
        assert path is not None
        assert stats["success"] is True

    def test_find_path_different_heuristics_same_result(self, pathfinder, simple_grid):
        """Test that different heuristics find paths of same length."""
        heuristics = ["manhattan", "euclidean", "chebyshev"]
        paths = []
        for h in heuristics:
            path, _ = pathfinder.find_path(
                simple_grid, (0, 0), (4, 4), h
            )
            paths.append(len(path))
        assert all(p == paths[0] for p in paths)
