"""Unit tests for depth-first search module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Graph, DFS


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


class TestDFS:
    """Test cases for DFS class."""

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
    def dfs(self, config_file):
        """Create DFS instance."""
        return DFS(config_path=config_file)

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

        dfs = DFS(config_path=str(config_path))
        assert dfs.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            DFS(config_path="nonexistent.yaml")

    def test_dfs_recursive_simple(self, dfs, simple_graph):
        """Test recursive DFS on simple graph."""
        path = dfs.dfs_recursive(simple_graph, 0)
        assert 0 in path
        assert len(path) > 0

    def test_dfs_recursive_all_vertices(self, dfs, simple_graph):
        """Test recursive DFS visits all vertices."""
        path = dfs.dfs_recursive(simple_graph, 0)
        assert len(path) == 5  # All 5 vertices

    def test_dfs_recursive_invalid_start(self, dfs, simple_graph):
        """Test recursive DFS with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            dfs.dfs_recursive(simple_graph, 999)

    def test_dfs_iterative_simple(self, dfs, simple_graph):
        """Test iterative DFS on simple graph."""
        path = dfs.dfs_iterative(simple_graph, 0)
        assert 0 in path
        assert len(path) > 0

    def test_dfs_iterative_all_vertices(self, dfs, simple_graph):
        """Test iterative DFS visits all vertices."""
        path = dfs.dfs_iterative(simple_graph, 0)
        assert len(path) == 5  # All 5 vertices

    def test_dfs_iterative_invalid_start(self, dfs, simple_graph):
        """Test iterative DFS with invalid start vertex."""
        with pytest.raises(ValueError, match="not in graph"):
            dfs.dfs_iterative(simple_graph, 999)

    def test_dfs_recursive_vs_iterative(self, dfs, simple_graph):
        """Test that recursive and iterative produce same results."""
        recursive_path = dfs.dfs_recursive(simple_graph, 0)
        iterative_path = dfs.dfs_iterative(simple_graph, 0)

        # Both should visit all vertices
        assert set(recursive_path) == set(iterative_path)
        assert len(recursive_path) == len(iterative_path)

    def test_dfs_all_components_single(self, dfs, simple_graph):
        """Test finding all components with single component."""
        components = dfs.dfs_all_components(simple_graph, method="recursive")
        assert len(components) == 1
        assert len(components[0]) == 5

    def test_dfs_all_components_multiple(self, dfs):
        """Test finding all components with multiple components."""
        graph = Graph()
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(4, 5)
        graph.add_vertex(6)

        components = dfs.dfs_all_components(graph, method="recursive")
        assert len(components) == 3

    def test_find_path_exists(self, dfs, simple_graph):
        """Test finding path when path exists."""
        path = dfs.find_path(simple_graph, 0, 3, method="recursive")
        assert path is not None
        assert path[0] == 0
        assert path[-1] == 3

    def test_find_path_not_exists(self, dfs):
        """Test finding path when path doesn't exist."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_vertex(2)

        path = dfs.find_path(graph, 0, 2, method="recursive")
        assert path is None

    def test_find_path_iterative(self, dfs, simple_graph):
        """Test finding path using iterative method."""
        path = dfs.find_path(simple_graph, 0, 4, method="iterative")
        assert path is not None
        assert path[0] == 0
        assert path[-1] == 4

    def test_compare_methods(self, dfs, simple_graph):
        """Test method comparison."""
        results = dfs.compare_methods(simple_graph, 0)

        assert "recursive" in results
        assert "iterative" in results
        assert "paths_match" in results
        assert results["paths_match"] is True

    def test_compare_methods_execution_time(self, dfs, simple_graph):
        """Test that comparison includes execution time."""
        results = dfs.compare_methods(simple_graph, 0)

        assert "execution_time" in results["recursive"]
        assert "execution_time" in results["iterative"]
        assert results["recursive"]["execution_time"] >= 0
        assert results["iterative"]["execution_time"] >= 0

    def test_generate_report(self, dfs, simple_graph, temp_dir):
        """Test report generation."""
        comparison = dfs.compare_methods(simple_graph, 0)
        report_path = temp_dir / "report.txt"
        report = dfs.generate_report(
            simple_graph, 0, comparison, output_path=str(report_path)
        )

        assert report_path.exists()
        assert "DEPTH-FIRST SEARCH" in report
        assert "RECURSIVE" in report
        assert "ITERATIVE" in report

    def test_dfs_directed_graph(self, dfs):
        """Test DFS on directed graph."""
        graph = Graph(directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(0, 3)

        path = dfs.dfs_recursive(graph, 0)
        assert 0 in path
        assert 1 in path
        assert 2 in path
        assert 3 in path

    def test_dfs_single_vertex(self, dfs):
        """Test DFS on graph with single vertex."""
        graph = Graph()
        graph.add_vertex(0)

        path = dfs.dfs_recursive(graph, 0)
        assert path == [0]

        path = dfs.dfs_iterative(graph, 0)
        assert path == [0]

    def test_dfs_empty_graph(self, dfs):
        """Test DFS on empty graph."""
        graph = Graph()
        with pytest.raises(ValueError):
            dfs.dfs_recursive(graph, 0)

    def test_dfs_disconnected_graph(self, dfs):
        """Test DFS on disconnected graph."""
        graph = Graph()
        graph.add_vertex(0)
        graph.add_vertex(1)

        path = dfs.dfs_recursive(graph, 0)
        assert path == [0]

    def test_dfs_string_vertices(self, dfs):
        """Test DFS with string vertices."""
        graph = Graph()
        graph.add_edge("A", "B")
        graph.add_edge("B", "C")

        path = dfs.dfs_recursive(graph, "A")
        assert "A" in path
        assert "B" in path
        assert "C" in path

    def test_dfs_large_graph(self, dfs):
        """Test DFS on larger graph."""
        graph = Graph()
        for i in range(10):
            graph.add_edge(i, i + 1)

        path = dfs.dfs_recursive(graph, 0)
        assert len(path) == 11

    def test_dfs_cycle(self, dfs):
        """Test DFS on graph with cycle."""
        graph = Graph()
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)

        path = dfs.dfs_recursive(graph, 0)
        assert len(path) == 3
        assert set(path) == {0, 1, 2}
