"""Unit tests for blossom algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BlossomAlgorithm


class TestBlossomAlgorithm:
    """Test cases for BlossomAlgorithm class."""

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

    def test_algorithm_creation(self, config_file):
        """Test BlossomAlgorithm creation."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        assert blossom.num_vertices == 5
        assert len(blossom.graph) == 5

    def test_add_edge(self, config_file):
        """Test adding edge."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        blossom.add_edge(0, 1)

        assert 1 in blossom.graph[0]
        assert 0 in blossom.graph[1]

    def test_add_edge_invalid_vertices(self, config_file):
        """Test adding edge with invalid vertices."""
        blossom = BlossomAlgorithm(5, config_path=config_file)

        with pytest.raises(ValueError):
            blossom.add_edge(-1, 1)

        with pytest.raises(ValueError):
            blossom.add_edge(0, 10)

    def test_add_edge_self_loop(self, config_file):
        """Test adding self-loop (should be ignored)."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        blossom.add_edge(0, 0)

        assert 0 not in blossom.graph[0]

    def test_find_maximum_matching_simple(self, config_file):
        """Test finding maximum matching on simple graph."""
        blossom = BlossomAlgorithm(4, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(2, 3)

        matching = blossom.find_maximum_matching()
        assert len(matching) == 2
        assert blossom.get_matching_size() == 2

    def test_find_maximum_matching_path(self, config_file):
        """Test finding maximum matching on path graph."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(1, 2)
        blossom.add_edge(2, 3)
        blossom.add_edge(3, 4)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 2

    def test_find_maximum_matching_cycle(self, config_file):
        """Test finding maximum matching on cycle graph."""
        blossom = BlossomAlgorithm(6, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(1, 2)
        blossom.add_edge(2, 3)
        blossom.add_edge(3, 4)
        blossom.add_edge(4, 5)
        blossom.add_edge(5, 0)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 3

    def test_find_maximum_matching_complete(self, config_file):
        """Test finding maximum matching on complete graph."""
        blossom = BlossomAlgorithm(4, config_path=config_file)
        for i in range(4):
            for j in range(i + 1, 4):
                blossom.add_edge(i, j)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 2

    def test_is_matched(self, config_file):
        """Test checking if vertex is matched."""
        blossom = BlossomAlgorithm(4, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(2, 3)

        blossom.find_maximum_matching()

        assert blossom.is_matched(0) is True
        assert blossom.is_matched(1) is True
        assert blossom.is_matched(2) is True
        assert blossom.is_matched(3) is True

    def test_is_matched_invalid_vertex(self, config_file):
        """Test is_matched with invalid vertex."""
        blossom = BlossomAlgorithm(4, config_path=config_file)

        with pytest.raises(ValueError):
            blossom.is_matched(-1)

        with pytest.raises(ValueError):
            blossom.is_matched(10)

    def test_get_matched_vertex(self, config_file):
        """Test getting matched vertex."""
        blossom = BlossomAlgorithm(4, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(2, 3)

        blossom.find_maximum_matching()

        assert blossom.get_matched_vertex(0) == 1
        assert blossom.get_matched_vertex(1) == 0
        assert blossom.get_matched_vertex(2) == 3
        assert blossom.get_matched_vertex(3) == 2

    def test_get_matched_vertex_invalid(self, config_file):
        """Test get_matched_vertex with invalid vertex."""
        blossom = BlossomAlgorithm(4, config_path=config_file)

        with pytest.raises(ValueError):
            blossom.get_matched_vertex(-1)

    def test_empty_graph(self, config_file):
        """Test on empty graph."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        matching = blossom.find_maximum_matching()

        assert len(matching) == 0
        assert blossom.get_matching_size() == 0

    def test_single_edge(self, config_file):
        """Test on graph with single edge."""
        blossom = BlossomAlgorithm(2, config_path=config_file)
        blossom.add_edge(0, 1)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 1
        assert (0, 1) in matching.items() or (1, 0) in matching.items()

    def test_star_graph(self, config_file):
        """Test on star graph."""
        blossom = BlossomAlgorithm(5, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(0, 2)
        blossom.add_edge(0, 3)
        blossom.add_edge(0, 4)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 2

    def test_triangle(self, config_file):
        """Test on triangle graph."""
        blossom = BlossomAlgorithm(3, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(1, 2)
        blossom.add_edge(2, 0)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() == 1

    def test_complex_graph(self, config_file):
        """Test on complex graph."""
        blossom = BlossomAlgorithm(6, config_path=config_file)
        blossom.add_edge(0, 1)
        blossom.add_edge(1, 2)
        blossom.add_edge(2, 3)
        blossom.add_edge(3, 4)
        blossom.add_edge(4, 5)
        blossom.add_edge(5, 0)
        blossom.add_edge(1, 3)

        matching = blossom.find_maximum_matching()
        assert blossom.get_matching_size() >= 2
