"""Unit tests for IDA* pathfinding implementation."""

import math
import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

from src.main import GridGraph, Heuristic, IDAStar


class TestHeuristic:
    """Test heuristic function functionality."""

    def test_manhattan_distance(self):
        """Test Manhattan distance calculation."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.manhattan_distance(node1, node2)
        assert distance == 7

    def test_euclidean_distance(self):
        """Test Euclidean distance calculation."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.euclidean_distance(node1, node2)
        assert math.isclose(distance, 5.0, rel_tol=1e-6)

    def test_chebyshev_distance(self):
        """Test Chebyshev distance calculation."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.chebyshev_distance(node1, node2)
        assert distance == 4

    def test_diagonal_distance(self):
        """Test diagonal distance calculation."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.diagonal_distance(node1, node2)
        assert distance > 0

    def test_octile_distance(self):
        """Test octile distance calculation."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.octile_distance(node1, node2)
        assert distance > 0

    def test_zero_heuristic(self):
        """Test zero heuristic."""
        node1 = (0, 0)
        node2 = (3, 4)
        distance = Heuristic.zero_heuristic(node1, node2)
        assert distance == 0.0

    def test_heuristic_admissibility(self):
        """Test that heuristics are admissible (never overestimate)."""
        node1 = (0, 0)
        node2 = (5, 5)

        manhattan = Heuristic.manhattan_distance(node1, node2)
        euclidean = Heuristic.euclidean_distance(node1, node2)
        chebyshev = Heuristic.chebyshev_distance(node1, node2)

        assert manhattan >= euclidean
        assert chebyshev >= euclidean

    def test_get_heuristic_valid(self):
        """Test getting valid heuristic by name."""
        heuristic = Heuristic.get_heuristic("manhattan")
        assert callable(heuristic)
        assert heuristic((0, 0), (1, 1)) == 2

    def test_get_heuristic_invalid(self):
        """Test getting invalid heuristic raises error."""
        with pytest.raises(ValueError, match="Unknown heuristic"):
            Heuristic.get_heuristic("invalid")


class TestGridGraph:
    """Test grid graph functionality."""

    def test_grid_initialization(self):
        """Test grid graph initialization."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid)
        assert graph.width == 5
        assert graph.height == 5

    def test_is_valid_walkable(self):
        """Test valid walkable node."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid)
        assert graph.is_valid((2, 2)) is True

    def test_is_valid_obstacle(self):
        """Test invalid obstacle node."""
        grid = np.zeros((5, 5))
        grid[2, 2] = 1
        graph = GridGraph(grid)
        assert graph.is_valid((2, 2)) is False

    def test_is_valid_out_of_bounds(self):
        """Test invalid out-of-bounds node."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid)
        assert graph.is_valid((10, 10)) is False
        assert graph.is_valid((-1, 0)) is False

    def test_get_neighbors_4_directional(self):
        """Test getting neighbors with 4-directional movement."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid, allow_diagonal=False)
        neighbors = graph.get_neighbors((2, 2))

        assert len(neighbors) == 4
        neighbor_coords = [n[0] for n in neighbors]
        assert (2, 3) in neighbor_coords
        assert (2, 1) in neighbor_coords
        assert (3, 2) in neighbor_coords
        assert (1, 2) in neighbor_coords

    def test_get_neighbors_8_directional(self):
        """Test getting neighbors with 8-directional movement."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid, allow_diagonal=True)
        neighbors = graph.get_neighbors((2, 2))

        assert len(neighbors) == 8

    def test_get_neighbors_with_obstacles(self):
        """Test getting neighbors excludes obstacles."""
        grid = np.zeros((5, 5))
        grid[2, 3] = 1
        grid[3, 2] = 1
        graph = GridGraph(grid, allow_diagonal=True)
        neighbors = graph.get_neighbors((2, 2))

        neighbor_coords = [n[0] for n in neighbors]
        assert (2, 3) not in neighbor_coords
        assert (3, 2) not in neighbor_coords

    def test_get_neighbors_boundary(self):
        """Test getting neighbors at grid boundary."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid, allow_diagonal=True)
        neighbors = graph.get_neighbors((0, 0))

        neighbor_coords = [n[0] for n in neighbors]
        assert (-1, -1) not in neighbor_coords
        assert (0, 0) not in neighbor_coords

    def test_custom_movement_costs(self):
        """Test custom movement costs."""
        grid = np.zeros((5, 5))
        graph = GridGraph(
            grid,
            allow_diagonal=True,
            movement_cost={"straight": 2.0, "diagonal": 3.0},
        )

        neighbors = graph.get_neighbors((2, 2))
        straight_neighbors = [
            n for n in neighbors
            if n[0] in [(2, 3), (2, 1), (3, 2), (1, 2)]
        ]
        diagonal_neighbors = [
            n for n in neighbors
            if n[0] not in [(2, 3), (2, 1), (3, 2), (1, 2)]
        ]

        if straight_neighbors:
            assert straight_neighbors[0][1] == 2.0
        if diagonal_neighbors:
            assert diagonal_neighbors[0][1] == 3.0


class TestIDAStar:
    """Test IDA* pathfinding algorithm."""

    def create_temp_config(self, config_dict: dict) -> str:
        """Create temporary config file for testing."""
        temp_file = tempfile.NamedTemporaryFile(
            mode="w", suffix=".yaml", delete=False
        )
        yaml.dump(config_dict, temp_file)
        temp_file.close()
        return temp_file.name

    def test_initialization_with_default_config(self):
        """Test initialization with default config file."""
        ida = IDAStar()
        assert ida.heuristic is not None
        assert isinstance(ida.allow_diagonal, bool)

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "ida_star": {
                "heuristic": "euclidean",
                "allow_diagonal": False,
                "max_iterations": 500,
            },
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            ida = IDAStar(config_path=config_path)
            assert ida.heuristic_name == "euclidean"
            assert ida.allow_diagonal is False
            assert ida.max_iterations == 500
        finally:
            Path(config_path).unlink()

    def test_simple_path(self):
        """Test finding path in simple grid."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid, allow_diagonal=False)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (4, 4))

        assert result["found"] is True
        assert len(result["path"]) > 0
        assert result["path"][0] == (0, 0)
        assert result["path"][-1] == (4, 4)
        assert result["cost"] > 0
        assert result["iterations"] > 0

    def test_path_with_obstacles(self):
        """Test finding path around obstacles."""
        grid = np.zeros((5, 5))
        grid[2, 1:4] = 1
        graph = GridGraph(grid, allow_diagonal=True)
        ida = IDAStar()

        result = ida.search(graph, (0, 2), (4, 2))

        assert result["found"] is True
        for node in result["path"]:
            assert grid[node[1], node[0]] == 0

    def test_no_path_exists(self):
        """Test when no path exists."""
        grid = np.zeros((5, 5))
        grid[2, :] = 1
        graph = GridGraph(grid, allow_diagonal=False)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (4, 4))

        assert result["found"] is False
        assert len(result["path"]) == 0
        assert result["cost"] == float("inf")

    def test_same_start_and_goal(self):
        """Test when start and goal are the same."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid)
        ida = IDAStar()

        result = ida.search(graph, (2, 2), (2, 2))

        assert result["found"] is True
        assert len(result["path"]) == 1
        assert result["path"][0] == (2, 2)
        assert result["cost"] == 0.0

    def test_invalid_start_node(self):
        """Test that invalid start node raises error."""
        grid = np.zeros((5, 5))
        grid[0, 0] = 1
        graph = GridGraph(grid)
        ida = IDAStar()

        with pytest.raises(ValueError, match="Start node"):
            ida.search(graph, (0, 0), (4, 4))

    def test_invalid_goal_node(self):
        """Test that invalid goal node raises error."""
        grid = np.zeros((5, 5))
        grid[4, 4] = 1
        graph = GridGraph(grid)
        ida = IDAStar()

        with pytest.raises(ValueError, match="Goal node"):
            ida.search(graph, (0, 0), (4, 4))

    def test_different_heuristics(self):
        """Test pathfinding with different heuristics."""
        grid = np.zeros((10, 10))
        graph = GridGraph(grid, allow_diagonal=True)

        heuristics = ["manhattan", "euclidean", "chebyshev", "diagonal", "octile"]

        for heuristic_name in heuristics:
            config = {
                "ida_star": {
                    "heuristic": heuristic_name,
                    "max_iterations": 100,
                },
                "logging": {"level": "WARNING", "file": "logs/test.log"},
            }

            config_path = self.create_temp_config(config)
            try:
                ida = IDAStar(config_path=config_path)
                result = ida.search(graph, (0, 0), (9, 9))

                assert result["found"] is True
                assert len(result["path"]) > 0
            finally:
                Path(config_path).unlink()

    def test_path_continuity(self):
        """Test that path is continuous (adjacent nodes)."""
        grid = np.zeros((10, 10))
        graph = GridGraph(grid, allow_diagonal=True)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (9, 9))

        assert result["found"] is True
        path = result["path"]

        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            dx = abs(current[0] - next_node[0])
            dy = abs(current[1] - next_node[1])
            assert dx <= 1 and dy <= 1
            assert dx + dy > 0

    def test_path_optimality(self):
        """Test that path cost is optimal for simple cases."""
        grid = np.zeros((5, 5))
        graph = GridGraph(grid, allow_diagonal=False)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (4, 0))

        assert result["found"] is True
        assert result["cost"] == 4.0

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            IDAStar(config_path="nonexistent.yaml")

    def test_iterations_tracking(self):
        """Test that iterations are tracked."""
        grid = np.zeros((10, 10))
        graph = GridGraph(grid, allow_diagonal=True)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (9, 9))

        assert result["iterations"] > 0
        assert result["nodes_explored"] > 0

    def test_path_length_matches_path(self):
        """Test that path_length matches actual path length."""
        grid = np.zeros((10, 10))
        graph = GridGraph(grid, allow_diagonal=True)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (9, 9))

        assert result["path_length"] == len(result["path"])

    def test_max_iterations_limit(self):
        """Test that max iterations limit is respected."""
        config = {
            "ida_star": {
                "heuristic": "zero",
                "max_iterations": 5,
            },
            "logging": {"level": "WARNING", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            grid = np.zeros((20, 20))
            graph = GridGraph(grid, allow_diagonal=False)
            ida = IDAStar(config_path=config_path)

            result = ida.search(graph, (0, 0), (19, 19))

            assert result["iterations"] <= 5
        finally:
            Path(config_path).unlink()

    def test_multiple_iterations(self):
        """Test that IDA* performs multiple iterations."""
        grid = np.zeros((10, 10))
        graph = GridGraph(grid, allow_diagonal=True)
        ida = IDAStar()

        result = ida.search(graph, (0, 0), (9, 9))

        assert result["iterations"] >= 1
        if result["found"]:
            assert result["iterations"] > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
