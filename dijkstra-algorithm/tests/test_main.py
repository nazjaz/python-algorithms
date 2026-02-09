"""Unit tests for Dijkstra's algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import WeightedGraph, Dijkstra


class TestWeightedGraph:
    """Test cases for WeightedGraph class."""

    def test_graph_initialization_undirected(self):
        """Test undirected graph initialization."""
        graph = WeightedGraph(directed=False)
        assert graph.directed is False
        assert len(graph.adjacency_list) == 0

    def test_graph_initialization_directed(self):
        """Test directed graph initialization."""
        graph = WeightedGraph(directed=True)
        assert graph.directed is True

    def test_add_edge_undirected(self):
        """Test adding edge to undirected graph."""
        graph = WeightedGraph(directed=False)
        graph.add_edge(0, 1, 5.0)
        neighbors = graph.get_neighbors(0)
        assert any(n == 1 and w == 5.0 for n, w in neighbors)
        neighbors = graph.get_neighbors(1)
        assert any(n == 0 and w == 5.0 for n, w in neighbors)

    def test_add_edge_directed(self):
        """Test adding edge to directed graph."""
        graph = WeightedGraph(directed=True)
        graph.add_edge(0, 1, 5.0)
        neighbors = graph.get_neighbors(0)
        assert any(n == 1 and w == 5.0 for n, w in neighbors)
        neighbors = graph.get_neighbors(1)
        assert len(neighbors) == 0

    def test_add_vertex(self):
        """Test adding vertex."""
        graph = WeightedGraph()
        graph.add_vertex(0)
        assert 0 in graph.get_vertices()

    def test_get_vertices(self):
        """Test getting all vertices."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 2.0)
        vertices = graph.get_vertices()
        assert 0 in vertices
        assert 1 in vertices
        assert 2 in vertices

    def test_get_neighbors(self):
        """Test getting neighbors with weights."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 5.0)
        graph.add_edge(0, 2, 3.0)
        neighbors = graph.get_neighbors(0)
        assert len(neighbors) == 2
        neighbor_dict = {n: w for n, w in neighbors}
        assert neighbor_dict[1] == 5.0
        assert neighbor_dict[2] == 3.0

    def test_get_neighbors_nonexistent(self):
        """Test getting neighbors of non-existent vertex."""
        graph = WeightedGraph()
        neighbors = graph.get_neighbors(999)
        assert neighbors == []

    def test_visualize(self):
        """Test graph visualization."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 5.0)
        visualization = graph.visualize()
        assert "Weighted Graph Structure" in visualization
        assert "0" in visualization


class TestDijkstra:
    """Test cases for Dijkstra class."""

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
    def dijkstra(self, config_file):
        """Create Dijkstra instance."""
        return Dijkstra(config_path=config_file)

    @pytest.fixture
    def simple_graph(self):
        """Create simple test graph."""
        graph = WeightedGraph(directed=False)
        graph.add_edge(0, 1, 4.0)
        graph.add_edge(0, 2, 1.0)
        graph.add_edge(1, 3, 1.0)
        graph.add_edge(2, 3, 5.0)
        return graph

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        dijkstra = Dijkstra(config_path=str(config_path))
        assert dijkstra.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            Dijkstra(config_path="nonexistent.yaml")

    def test_shortest_path_exists(self, dijkstra, simple_graph):
        """Test shortest path when path exists."""
        path, distance = dijkstra.shortest_path(simple_graph, 0, 3)
        assert path is not None
        assert path[0] == 0
        assert path[-1] == 3
        assert distance > 0

    def test_shortest_path_same_vertex(self, dijkstra, simple_graph):
        """Test shortest path when start equals target."""
        path, distance = dijkstra.shortest_path(simple_graph, 0, 0)
        assert path == [0]
        assert distance == 0.0

    def test_shortest_path_not_exists(self, dijkstra):
        """Test shortest path when path doesn't exist."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 1.0)
        graph.add_vertex(2)

        path, distance = dijkstra.shortest_path(graph, 0, 2)
        assert path is None
        assert distance == float('inf')

    def test_shortest_path_invalid_start(self, dijkstra, simple_graph):
        """Test shortest path with invalid start vertex."""
        with pytest.raises(ValueError, match="Start vertex"):
            dijkstra.shortest_path(simple_graph, 999, 3)

    def test_shortest_path_invalid_target(self, dijkstra, simple_graph):
        """Test shortest path with invalid target vertex."""
        with pytest.raises(ValueError, match="Target vertex"):
            dijkstra.shortest_path(simple_graph, 0, 999)

    def test_shortest_path_optimal(self, dijkstra):
        """Test that Dijkstra finds optimal path."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 4.0)
        graph.add_edge(0, 2, 1.0)
        graph.add_edge(1, 3, 1.0)
        graph.add_edge(2, 3, 5.0)

        path, distance = dijkstra.shortest_path(graph, 0, 3)
        # Optimal path: 0 -> 2 -> 3 (distance 6) is longer than 0 -> 1 -> 3 (distance 5)
        # Actually wait, let me recalculate:
        # 0 -> 1 -> 3: 4 + 1 = 5
        # 0 -> 2 -> 3: 1 + 5 = 6
        # So optimal is 0 -> 1 -> 3 with distance 5
        assert distance == 5.0
        assert path[0] == 0
        assert path[-1] == 3

    def test_shortest_distances(self, dijkstra, simple_graph):
        """Test shortest distances to all vertices."""
        distances = dijkstra.shortest_distances(simple_graph, 0)
        assert distances[0] == 0.0
        assert distances[1] == 4.0
        assert distances[2] == 1.0
        assert distances[3] == 5.0  # 0 -> 1 -> 3 = 4 + 1 = 5

    def test_shortest_distances_invalid_start(self, dijkstra, simple_graph):
        """Test shortest distances with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            dijkstra.shortest_distances(simple_graph, 999)

    def test_shortest_paths_from_source(self, dijkstra, simple_graph):
        """Test finding all shortest paths from source."""
        paths = dijkstra.shortest_paths_from_source(simple_graph, 0)
        assert 0 in paths
        assert 1 in paths
        assert 2 in paths
        assert 3 in paths

        path_0, dist_0 = paths[0]
        assert path_0 == [0]
        assert dist_0 == 0.0

    def test_dijkstra_directed_graph(self, dijkstra):
        """Test Dijkstra on directed graph."""
        graph = WeightedGraph(directed=True)
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 2.0)
        graph.add_edge(0, 3, 4.0)

        path, distance = dijkstra.shortest_path(graph, 0, 2)
        assert path is not None
        assert distance == 3.0

    def test_dijkstra_single_vertex(self, dijkstra):
        """Test Dijkstra on graph with single vertex."""
        graph = WeightedGraph()
        graph.add_vertex(0)

        path, distance = dijkstra.shortest_path(graph, 0, 0)
        assert path == [0]
        assert distance == 0.0

    def test_dijkstra_empty_graph(self, dijkstra):
        """Test Dijkstra on empty graph."""
        graph = WeightedGraph()
        with pytest.raises(ValueError):
            dijkstra.shortest_path(graph, 0, 1)

    def test_dijkstra_disconnected_graph(self, dijkstra):
        """Test Dijkstra on disconnected graph."""
        graph = WeightedGraph()
        graph.add_vertex(0)
        graph.add_vertex(1)

        path, distance = dijkstra.shortest_path(graph, 0, 1)
        assert path is None
        assert distance == float('inf')

    def test_dijkstra_string_vertices(self, dijkstra):
        """Test Dijkstra with string vertices."""
        graph = WeightedGraph()
        graph.add_edge("A", "B", 2.0)
        graph.add_edge("B", "C", 3.0)

        path, distance = dijkstra.shortest_path(graph, "A", "C")
        assert path == ["A", "B", "C"]
        assert distance == 5.0

    def test_dijkstra_large_graph(self, dijkstra):
        """Test Dijkstra on larger graph."""
        graph = WeightedGraph()
        for i in range(10):
            graph.add_edge(i, i + 1, 1.0)

        path, distance = dijkstra.shortest_path(graph, 0, 10)
        assert distance == 10.0
        assert len(path) == 11

    def test_dijkstra_multiple_paths(self, dijkstra):
        """Test Dijkstra when multiple paths exist."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(0, 2, 3.0)
        graph.add_edge(1, 3, 2.0)
        graph.add_edge(2, 3, 1.0)
        graph.add_edge(3, 4, 1.0)

        path, distance = dijkstra.shortest_path(graph, 0, 4)
        # Path 0 -> 1 -> 3 -> 4: 1 + 2 + 1 = 4
        # Path 0 -> 2 -> 3 -> 4: 3 + 1 + 1 = 5
        # Optimal is 0 -> 1 -> 3 -> 4 with distance 4
        assert distance == 4.0
        assert path[0] == 0
        assert path[-1] == 4

    def test_generate_report(self, dijkstra, simple_graph, temp_dir):
        """Test report generation."""
        report_path = temp_dir / "report.txt"
        report = dijkstra.generate_report(
            simple_graph, 0, target=3, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "DIJKSTRA'S ALGORITHM" in report
        assert "SHORTEST DISTANCES" in report
        assert "SHORTEST PATH" in report

    def test_shortest_distances_all_reachable(self, dijkstra):
        """Test that shortest distances finds all reachable vertices."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 1.0)
        graph.add_edge(1, 2, 2.0)
        graph.add_vertex(3)

        distances = dijkstra.shortest_distances(graph, 0)
        assert 0 in distances
        assert 1 in distances
        assert 2 in distances
        assert 3 not in distances  # Unreachable

    def test_priority_queue_optimization(self, dijkstra):
        """Test that priority queue correctly selects minimum distance."""
        graph = WeightedGraph()
        graph.add_edge(0, 1, 10.0)
        graph.add_edge(0, 2, 1.0)
        graph.add_edge(2, 1, 1.0)

        path, distance = dijkstra.shortest_path(graph, 0, 1)
        # Optimal: 0 -> 2 -> 1 = 1 + 1 = 2 (not 0 -> 1 = 10)
        assert distance == 2.0
        assert path == [0, 2, 1]
