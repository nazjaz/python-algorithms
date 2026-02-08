"""Unit tests for bidirectional Dijkstra implementation."""

import tempfile
from pathlib import Path

import numpy as np
import pytest
import yaml

from src.main import BidirectionalDijkstra, Graph


class TestGraph:
    """Test graph functionality."""

    def test_graph_from_adjacency_list(self):
        """Test graph initialization from adjacency list."""
        adjacency_list = {
            0: [(1, 1.0), (2, 2.0)],
            1: [(2, 3.0)],
            2: [],
        }
        graph = Graph(adjacency_list=adjacency_list)
        assert 0 in graph.nodes
        assert 1 in graph.nodes
        assert 2 in graph.nodes
        assert graph.is_grid is False

    def test_graph_from_grid(self):
        """Test graph initialization from grid."""
        grid = np.zeros((5, 5))
        graph = Graph(grid=grid, allow_diagonal=True)
        assert graph.is_grid is True
        assert graph.width == 5
        assert graph.height == 5
        assert (0, 0) in graph.nodes

    def test_graph_neighbors_adjacency_list(self):
        """Test getting neighbors from adjacency list."""
        adjacency_list = {
            0: [(1, 1.0), (2, 2.0)],
            1: [(2, 3.0)],
            2: [],
        }
        graph = Graph(adjacency_list=adjacency_list)
        neighbors = graph.get_neighbors(0)
        assert len(neighbors) == 2
        assert (1, 1.0) in neighbors
        assert (2, 2.0) in neighbors

    def test_graph_neighbors_grid(self):
        """Test getting neighbors from grid."""
        grid = np.zeros((5, 5))
        graph = Graph(grid=grid, allow_diagonal=False)
        neighbors = graph.get_neighbors((2, 2))
        assert len(neighbors) == 4

    def test_graph_neighbors_grid_diagonal(self):
        """Test getting neighbors from grid with diagonal."""
        grid = np.zeros((5, 5))
        graph = Graph(grid=grid, allow_diagonal=True)
        neighbors = graph.get_neighbors((2, 2))
        assert len(neighbors) == 8

    def test_graph_neighbors_with_obstacles(self):
        """Test getting neighbors excludes obstacles."""
        grid = np.zeros((5, 5))
        grid[2, 3] = 1
        grid[3, 2] = 1
        graph = Graph(grid=grid, allow_diagonal=True)
        neighbors = graph.get_neighbors((2, 2))
        neighbor_coords = [n[0] for n in neighbors]
        assert (3, 2) not in neighbor_coords
        assert (2, 3) not in neighbor_coords

    def test_graph_custom_movement_costs(self):
        """Test custom movement costs."""
        grid = np.zeros((5, 5))
        graph = Graph(
            grid=grid,
            allow_diagonal=True,
            movement_cost={"straight": 2.0, "diagonal": 3.0},
        )
        neighbors = graph.get_neighbors((2, 2))
        straight_neighbors = [
            n for n in neighbors
            if n[0] in [(2, 3), (2, 1), (3, 2), (1, 2)]
        ]
        if straight_neighbors:
            assert straight_neighbors[0][1] == 2.0

    def test_graph_no_input(self):
        """Test that graph requires input."""
        with pytest.raises(ValueError, match="Must provide"):
            Graph()


class TestBidirectionalDijkstra:
    """Test bidirectional Dijkstra algorithm."""

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
        dijkstra = BidirectionalDijkstra()
        assert dijkstra.max_iterations > 0

    def test_initialization_with_custom_config(self):
        """Test initialization with custom config file."""
        config = {
            "bidirectional_dijkstra": {"max_iterations": 5000},
            "logging": {"level": "INFO", "file": "logs/test.log"},
        }

        config_path = self.create_temp_config(config)
        try:
            dijkstra = BidirectionalDijkstra(config_path=config_path)
            assert dijkstra.max_iterations == 5000
        finally:
            Path(config_path).unlink()

    def test_simple_path_adjacency_list(self):
        """Test finding path in simple adjacency list graph."""
        adjacency_list = {
            0: [(1, 1.0), (2, 4.0)],
            1: [(2, 2.0), (3, 5.0)],
            2: [(3, 1.0)],
            3: [],
        }
        graph = Graph(adjacency_list=adjacency_list)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, 0, 3)

        assert result["found"] is True
        assert len(result["path"]) > 0
        assert result["path"][0] == 0
        assert result["path"][-1] == 3
        assert result["cost"] > 0

    def test_simple_path_grid(self):
        """Test finding path in simple grid."""
        grid = np.zeros((5, 5))
        graph = Graph(grid=grid, allow_diagonal=False)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (4, 4))

        assert result["found"] is True
        assert len(result["path"]) > 0
        assert result["path"][0] == (0, 0)
        assert result["path"][-1] == (4, 4)
        assert result["cost"] > 0

    def test_path_with_obstacles(self):
        """Test finding path around obstacles."""
        grid = np.zeros((5, 5))
        grid[2, 1:4] = 1
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 2), (4, 2))

        assert result["found"] is True
        for node in result["path"]:
            assert grid[node[1], node[0]] == 0

    def test_no_path_exists(self):
        """Test when no path exists."""
        grid = np.zeros((5, 5))
        grid[2, :] = 1
        graph = Graph(grid=grid, allow_diagonal=False)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (4, 4))

        assert result["found"] is False
        assert len(result["path"]) == 0
        assert result["cost"] == float("inf")

    def test_same_start_and_goal(self):
        """Test when start and goal are the same."""
        grid = np.zeros((5, 5))
        graph = Graph(grid=grid)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (2, 2), (2, 2))

        assert result["found"] is True
        assert len(result["path"]) == 1
        assert result["path"][0] == (2, 2)
        assert result["cost"] == 0.0

    def test_invalid_start_node(self):
        """Test that invalid start node raises error."""
        grid = np.zeros((5, 5))
        grid[0, 0] = 1
        graph = Graph(grid=grid)
        dijkstra = BidirectionalDijkstra()

        with pytest.raises(ValueError, match="Start node"):
            dijkstra.search(graph, (0, 0), (4, 4))

    def test_invalid_goal_node(self):
        """Test that invalid goal node raises error."""
        grid = np.zeros((5, 5))
        grid[4, 4] = 1
        graph = Graph(grid=grid)
        dijkstra = BidirectionalDijkstra()

        with pytest.raises(ValueError, match="Goal node"):
            dijkstra.search(graph, (0, 0), (4, 4))

    def test_path_continuity(self):
        """Test that path is continuous (adjacent nodes)."""
        grid = np.zeros((10, 10))
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (9, 9))

        assert result["found"] is True
        path = result["path"]

        for i in range(len(path) - 1):
            current = path[i]
            next_node = path[i + 1]
            if graph.is_grid:
                dx = abs(current[0] - next_node[0])
                dy = abs(current[1] - next_node[1])
                assert dx <= 1 and dy <= 1
                assert dx + dy > 0

    def test_path_optimality(self):
        """Test that path cost is optimal for simple cases."""
        adjacency_list = {
            0: [(1, 1.0), (2, 5.0)],
            1: [(2, 1.0)],
            2: [],
        }
        graph = Graph(adjacency_list=adjacency_list)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, 0, 2)

        assert result["found"] is True
        assert result["cost"] == 2.0

    def test_config_file_not_found(self):
        """Test that missing config file raises error."""
        with pytest.raises(FileNotFoundError):
            BidirectionalDijkstra(config_path="nonexistent.yaml")

    def test_nodes_explored_tracking(self):
        """Test that nodes explored are tracked."""
        grid = np.zeros((10, 10))
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (9, 9))

        assert result["nodes_explored_forward"] > 0
        assert result["nodes_explored_backward"] > 0
        assert (
            result["nodes_explored"]
            == result["nodes_explored_forward"] + result["nodes_explored_backward"]
        )

    def test_path_length_matches_path(self):
        """Test that path_length matches actual path length."""
        grid = np.zeros((10, 10))
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (9, 9))

        assert result["path_length"] == len(result["path"])

    def test_meeting_node_tracking(self):
        """Test that meeting node is tracked."""
        grid = np.zeros((10, 10))
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (9, 9))

        if result["found"]:
            assert result["meeting_node"] is not None
            assert result["meeting_node"] in result["path"]

    def test_bidirectional_exploration(self):
        """Test that both directions are explored."""
        grid = np.zeros((20, 20))
        graph = Graph(grid=grid, allow_diagonal=False)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (19, 19))

        assert result["nodes_explored_forward"] > 0
        assert result["nodes_explored_backward"] > 0

    def test_weighted_graph(self):
        """Test pathfinding in weighted graph."""
        adjacency_list = {
            0: [(1, 10.0), (2, 1.0)],
            1: [(3, 1.0)],
            2: [(3, 1.0)],
            3: [],
        }
        graph = Graph(adjacency_list=adjacency_list)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, 0, 3)

        assert result["found"] is True
        assert result["cost"] == 2.0
        assert result["path"] == [0, 2, 3] or result["path"] == [0, 1, 3]

    def test_large_graph(self):
        """Test pathfinding in large graph."""
        grid = np.zeros((30, 30))
        graph = Graph(grid=grid, allow_diagonal=True)
        dijkstra = BidirectionalDijkstra()

        result = dijkstra.search(graph, (0, 0), (29, 29))

        assert result["found"] is True
        assert result["nodes_explored"] < 900


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
