"""Unit tests for breadth-first search module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Graph, BFS


class TestGraph:
    """Test cases for Graph class."""

    def test_graph_initialization_undirected(self):
        """Test undirected graph initialization."""
        graph = Graph(directed=False)
        assert graph.directed is False
        assert len(graph.adjacency_list) == 0

    def test_graph_initialization_directed(self):
        """Test directed graph initialization."""
        graph = Graph(directed=True)
        assert graph.directed is True

    def test_add_edge_undirected(self):
        """Test adding edge to undirected graph."""
        graph = Graph(directed=False)
        graph.add_edge(0, 1)
        assert 1 in graph.get_neighbors(0)
        assert 0 in graph.get_neighbors(1)

    def test_add_edge_directed(self):
        """Test adding edge to directed graph."""
        graph = Graph(directed=True)
        graph.add_edge(0, 1)
        assert 1 in graph.get_neighbors(0)
        assert 0 not in graph.get_neighbors(1)

    def test_add_vertex(self):
        """Test adding vertex."""
        graph = Graph()
        graph.add_vertex(0)
        assert 0 in graph.get_vertices()

    def test_get_vertices(self):
        """Test getting all vertices."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        vertices = graph.get_vertices()
        assert 0 in vertices
        assert 1 in vertices
        assert 2 in vertices

    def test_get_neighbors(self):
        """Test getting neighbors."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        neighbors = graph.get_neighbors(0)
        assert 1 in neighbors
        assert 2 in neighbors

    def test_get_neighbors_nonexistent(self):
        """Test getting neighbors of non-existent vertex."""
        graph = Graph()
        neighbors = graph.get_neighbors(999)
        assert neighbors == []

    def test_visualize(self):
        """Test graph visualization."""
        graph = Graph()
        graph.add_edge(0, 1)
        visualization = graph.visualize()
        assert "Graph Structure" in visualization
        assert "0" in visualization


class TestBFS:
    """Test cases for BFS class."""

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
    def bfs(self, config_file):
        """Create BFS instance."""
        return BFS(config_path=config_file)

    @pytest.fixture
    def simple_graph(self):
        """Create simple test graph."""
        graph = Graph(directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 4)
        return graph

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        bfs = BFS(config_path=str(config_path))
        assert bfs.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            BFS(config_path="nonexistent.yaml")

    def test_bfs_traversal_simple(self, bfs, simple_graph):
        """Test BFS traversal on simple graph."""
        traversal = bfs.bfs_traversal(simple_graph, 0)
        assert 0 in traversal
        assert len(traversal) > 0

    def test_bfs_traversal_all_vertices(self, bfs, simple_graph):
        """Test BFS traversal visits all vertices."""
        traversal = bfs.bfs_traversal(simple_graph, 0)
        assert len(traversal) == 5  # All 5 vertices

    def test_bfs_traversal_order(self, bfs, simple_graph):
        """Test BFS traversal order (level by level)."""
        traversal = bfs.bfs_traversal(simple_graph, 0)
        # Level 0: 0
        # Level 1: 1, 2
        # Level 2: 3, 4
        assert traversal[0] == 0
        assert set(traversal[1:3]) == {1, 2}
        assert set(traversal[3:5]) == {3, 4}

    def test_bfs_traversal_invalid_start(self, bfs, simple_graph):
        """Test BFS traversal with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            bfs.bfs_traversal(simple_graph, 999)

    def test_shortest_path_exists(self, bfs, simple_graph):
        """Test shortest path when path exists."""
        path, distance = bfs.shortest_path(simple_graph, 0, 3)
        assert path is not None
        assert path[0] == 0
        assert path[-1] == 3
        assert distance == 2

    def test_shortest_path_same_vertex(self, bfs, simple_graph):
        """Test shortest path when start equals target."""
        path, distance = bfs.shortest_path(simple_graph, 0, 0)
        assert path == [0]
        assert distance == 0

    def test_shortest_path_not_exists(self, bfs):
        """Test shortest path when path doesn't exist."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_vertex(2)

        path, distance = bfs.shortest_path(graph, 0, 2)
        assert path is None
        assert distance == -1

    def test_shortest_path_invalid_start(self, bfs, simple_graph):
        """Test shortest path with invalid start vertex."""
        with pytest.raises(ValueError, match="Start vertex"):
            bfs.shortest_path(simple_graph, 999, 3)

    def test_shortest_path_invalid_target(self, bfs, simple_graph):
        """Test shortest path with invalid target vertex."""
        with pytest.raises(ValueError, match="Target vertex"):
            bfs.shortest_path(simple_graph, 0, 999)

    def test_shortest_path_guarantees_shortest(self, bfs):
        """Test that BFS guarantees shortest path."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)

        path, distance = bfs.shortest_path(graph, 0, 3)
        # Shortest path should be 0 -> 1 -> 3 or 0 -> 2 -> 3 (distance 2)
        # Not 0 -> 1 -> 2 -> 3 or any longer path
        assert distance == 2
        assert len(path) == 3

    def test_shortest_distances(self, bfs, simple_graph):
        """Test shortest distances to all vertices."""
        distances = bfs.shortest_distances(simple_graph, 0)
        assert distances[0] == 0
        assert distances[1] == 1
        assert distances[2] == 1
        assert distances[3] == 2
        assert distances[4] == 2

    def test_shortest_distances_invalid_start(self, bfs, simple_graph):
        """Test shortest distances with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            bfs.shortest_distances(simple_graph, 999)

    def test_level_order_traversal(self, bfs, simple_graph):
        """Test level-order traversal."""
        levels = bfs.level_order_traversal(simple_graph, 0)
        assert len(levels) == 3
        assert levels[0] == [0]
        assert set(levels[1]) == {1, 2}
        assert set(levels[2]) == {3, 4}

    def test_level_order_traversal_invalid_start(self, bfs, simple_graph):
        """Test level-order traversal with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            bfs.level_order_traversal(simple_graph, 999)

    def test_bfs_all_components_single(self, bfs, simple_graph):
        """Test finding all components with single component."""
        components = bfs.bfs_all_components(simple_graph)
        assert len(components) == 1
        assert len(components[0]) == 5

    def test_bfs_all_components_multiple(self, bfs):
        """Test finding all components with multiple components."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(4, 5)
        graph.add_vertex(6)

        components = bfs.bfs_all_components(graph)
        assert len(components) == 3

    def test_bfs_directed_graph(self, bfs):
        """Test BFS on directed graph."""
        graph = Graph(directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(0, 3)

        traversal = bfs.bfs_traversal(graph, 0)
        assert 0 in traversal
        assert 1 in traversal
        assert 2 in traversal
        assert 3 in traversal

    def test_bfs_single_vertex(self, bfs):
        """Test BFS on graph with single vertex."""
        graph = Graph()
        graph.add_vertex(0)

        traversal = bfs.bfs_traversal(graph, 0)
        assert traversal == [0]

        path, distance = bfs.shortest_path(graph, 0, 0)
        assert path == [0]
        assert distance == 0

    def test_bfs_empty_graph(self, bfs):
        """Test BFS on empty graph."""
        graph = Graph()
        with pytest.raises(ValueError):
            bfs.bfs_traversal(graph, 0)

    def test_bfs_disconnected_graph(self, bfs):
        """Test BFS on disconnected graph."""
        graph = Graph()
        graph.add_vertex(0)
        graph.add_vertex(1)

        traversal = bfs.bfs_traversal(graph, 0)
        assert traversal == [0]

        path, distance = bfs.shortest_path(graph, 0, 1)
        assert path is None
        assert distance == -1

    def test_bfs_string_vertices(self, bfs):
        """Test BFS with string vertices."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")

        traversal = bfs.bfs_traversal(graph, "A")
        assert "A" in traversal
        assert "B" in traversal
        assert "C" in traversal

        path, distance = bfs.shortest_path(graph, "A", "C")
        assert path == ["A", "B", "C"]
        assert distance == 2

    def test_bfs_large_graph(self, bfs):
        """Test BFS on larger graph."""
        graph = Graph()
        for i in range(10):
            graph.add_edge(i, i + 1)

        traversal = bfs.bfs_traversal(graph, 0)
        assert len(traversal) == 11

        path, distance = bfs.shortest_path(graph, 0, 10)
        assert distance == 10
        assert len(path) == 11

    def test_bfs_cycle(self, bfs):
        """Test BFS on graph with cycle."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)

        traversal = bfs.bfs_traversal(graph, 0)
        assert len(traversal) == 3
        assert set(traversal) == {0, 1, 2}

    def test_generate_report(self, bfs, simple_graph, temp_dir):
        """Test report generation."""
        report_path = temp_dir / "report.txt"
        report = bfs.generate_report(
            simple_graph, 0, target=3, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "BREADTH-FIRST SEARCH" in report
        assert "BFS TRAVERSAL" in report
        assert "SHORTEST PATH" in report

    def test_shortest_path_multiple_paths(self, bfs):
        """Test shortest path when multiple paths exist."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(2, 3)
        graph.add_edge(3, 4)

        path, distance = bfs.shortest_path(graph, 0, 4)
        # Shortest path should be distance 3
        assert distance == 3
        assert path[0] == 0
        assert path[-1] == 4

    def test_level_order_traversal_complex(self, bfs):
        """Test level-order traversal on complex graph."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(1, 3)
        graph.add_edge(1, 4)
        graph.add_edge(2, 5)

        levels = bfs.level_order_traversal(graph, 0)
        assert len(levels) == 3
        assert levels[0] == [0]
        assert set(levels[1]) == {1, 2}
        assert set(levels[2]) == {3, 4, 5}
