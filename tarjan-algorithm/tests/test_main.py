"""Unit tests for Tarjan's algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import Graph, TarjanAlgorithm


class TestGraph:
    """Test cases for Graph class."""

    def test_graph_creation_directed(self):
        """Test directed graph creation."""
        graph = Graph(5, directed=True)
        assert graph.num_vertices == 5
        assert graph.directed is True

    def test_graph_creation_undirected(self):
        """Test undirected graph creation."""
        graph = Graph(5, directed=False)
        assert graph.num_vertices == 5
        assert graph.directed is False

    def test_add_edge_directed(self):
        """Test adding edge to directed graph."""
        graph = Graph(5, directed=True)
        graph.add_edge(0, 1)

        assert 1 in graph.adjacency_list[0]
        assert 0 not in graph.adjacency_list[1]

    def test_add_edge_undirected(self):
        """Test adding edge to undirected graph."""
        graph = Graph(5, directed=False)
        graph.add_edge(0, 1)

        assert 1 in graph.adjacency_list[0]
        assert 0 in graph.adjacency_list[1]

    def test_add_edge_invalid_vertices(self):
        """Test adding edge with invalid vertices."""
        graph = Graph(5)

        with pytest.raises(ValueError):
            graph.add_edge(-1, 1)

        with pytest.raises(ValueError):
            graph.add_edge(0, 10)


class TestTarjanAlgorithm:
    """Test cases for TarjanAlgorithm class."""

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

    def test_scc_simple_graph(self, config_file):
        """Test finding SCCs in simple graph."""
        graph = Graph(3, directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        sccs = tarjan.find_strongly_connected_components()

        assert len(sccs) >= 1
        assert tarjan.get_scc_count() == len(sccs)

    def test_scc_disconnected(self, config_file):
        """Test finding SCCs in disconnected graph."""
        graph = Graph(4, directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(2, 3)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        sccs = tarjan.find_strongly_connected_components()

        assert len(sccs) >= 2

    def test_scc_single_vertex(self, config_file):
        """Test finding SCCs with single vertex."""
        graph = Graph(1, directed=True)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        sccs = tarjan.find_strongly_connected_components()

        assert len(sccs) == 1

    def test_scc_undirected_graph_error(self, config_file):
        """Test SCC on undirected graph raises error."""
        graph = Graph(3, directed=False)
        graph.add_edge(0, 1)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        with pytest.raises(ValueError):
            tarjan.find_strongly_connected_components()

    def test_articulation_points_simple(self, config_file):
        """Test finding articulation points in simple graph."""
        graph = Graph(4, directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert isinstance(articulation_points, set)
        assert tarjan.get_articulation_point_count() == len(articulation_points)

    def test_articulation_points_cycle(self, config_file):
        """Test finding articulation points in cycle."""
        graph = Graph(4, directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(3, 0)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert len(articulation_points) == 0

    def test_articulation_points_star(self, config_file):
        """Test finding articulation points in star graph."""
        graph = Graph(5, directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(0, 2)
        graph.add_edge(0, 3)
        graph.add_edge(0, 4)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert 0 in articulation_points

    def test_articulation_points_directed_graph_error(self, config_file):
        """Test articulation points on directed graph raises error."""
        graph = Graph(3, directed=True)
        graph.add_edge(0, 1)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        with pytest.raises(ValueError):
            tarjan.find_articulation_points()

    def test_articulation_points_empty_graph(self, config_file):
        """Test finding articulation points in empty graph."""
        graph = Graph(3, directed=False)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert len(articulation_points) == 0

    def test_scc_complex_graph(self, config_file):
        """Test finding SCCs in complex graph."""
        graph = Graph(6, directed=True)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        graph.add_edge(1, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 5)
        graph.add_edge(5, 3)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        sccs = tarjan.find_strongly_connected_components()

        assert len(sccs) >= 1

    def test_articulation_points_complex_graph(self, config_file):
        """Test finding articulation points in complex graph."""
        graph = Graph(6, directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(2, 0)
        graph.add_edge(1, 3)
        graph.add_edge(3, 4)
        graph.add_edge(4, 5)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert isinstance(articulation_points, set)

    def test_scc_all_vertices_separate(self, config_file):
        """Test SCCs when all vertices are separate."""
        graph = Graph(5, directed=True)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        sccs = tarjan.find_strongly_connected_components()

        assert len(sccs) == 5

    def test_articulation_points_tree(self, config_file):
        """Test finding articulation points in tree."""
        graph = Graph(5, directed=False)
        graph.add_edge(0, 1)
        graph.add_edge(1, 2)
        graph.add_edge(1, 3)
        graph.add_edge(3, 4)

        tarjan = TarjanAlgorithm(graph, config_path=config_file)
        articulation_points = tarjan.find_articulation_points()

        assert 1 in articulation_points
        assert 3 in articulation_points
