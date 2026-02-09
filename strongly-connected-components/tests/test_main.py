"""Unit tests for strongly connected components module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import StronglyConnectedComponents


class TestStronglyConnectedComponents:
    """Test cases for StronglyConnectedComponents class."""

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
    def scc_finder(self, config_file):
        """Create StronglyConnectedComponents instance."""
        return StronglyConnectedComponents(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        scc_finder = StronglyConnectedComponents(config_path=str(config_path))
        assert scc_finder.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test configuration loading with missing file."""
        with pytest.raises(FileNotFoundError):
            StronglyConnectedComponents(config_path="nonexistent.yaml")

    def test_build_graph_empty_edges_no_vertices(self, scc_finder):
        """Test building graph with no edges and no vertices."""
        with pytest.raises(ValueError, match="must be provided"):
            scc_finder._build_graph([], None)

    def test_build_graph_empty_edges_with_vertices(self, scc_finder):
        """Test building graph with no edges but specified vertices."""
        adjacency_list, vertices = scc_finder._build_graph([], num_vertices=5)
        assert len(vertices) == 5
        assert all(v in adjacency_list for v in vertices)

    def test_build_graph_with_edges(self, scc_finder):
        """Test building graph with edges."""
        edges = [(0, 1), (1, 2), (2, 3)]
        adjacency_list, vertices = scc_finder._build_graph(edges)
        assert 0 in adjacency_list
        assert 1 in adjacency_list[0]
        assert len(vertices) == 4

    def test_build_graph_negative_vertex(self, scc_finder):
        """Test building graph with negative vertex index."""
        with pytest.raises(ValueError, match="non-negative"):
            scc_finder._build_graph([(-1, 0)])

    def test_transpose_graph(self, scc_finder):
        """Test transpose graph construction."""
        edges = [(0, 1), (1, 2), (2, 0)]
        adjacency_list, vertices = scc_finder._build_graph(edges)
        transpose = scc_finder._transpose_graph(adjacency_list, vertices)
        assert 0 in transpose[1]
        assert 1 in transpose[2]
        assert 2 in transpose[0]

    def test_find_sccs_simple_cycle(self, scc_finder):
        """Test finding SCCs with simple cycle."""
        edges = [(0, 1), (1, 2), (2, 0)]
        sccs = scc_finder.find_sccs(edges)
        assert len(sccs) == 1
        assert set(sccs[0]) == {0, 1, 2}

    def test_find_sccs_multiple_sccs(self, scc_finder):
        """Test finding SCCs with multiple components."""
        edges = [(0, 1), (1, 0), (2, 3), (3, 2)]
        sccs = scc_finder.find_sccs(edges)
        assert len(sccs) == 2
        scc_sets = [set(scc) for scc in sccs]
        assert {0, 1} in scc_sets
        assert {2, 3} in scc_sets

    def test_find_sccs_empty_graph(self, scc_finder):
        """Test finding SCCs with empty graph."""
        sccs = scc_finder.find_sccs([], num_vertices=0)
        assert sccs == []

    def test_find_sccs_single_vertex(self, scc_finder):
        """Test finding SCCs with single vertex."""
        sccs = scc_finder.find_sccs([], num_vertices=1)
        assert len(sccs) == 1
        assert sccs[0] == [0]

    def test_find_sccs_isolated_vertices(self, scc_finder):
        """Test finding SCCs with isolated vertices."""
        edges = []
        sccs = scc_finder.find_sccs(edges, num_vertices=5)
        assert len(sccs) == 5
        for scc in sccs:
            assert len(scc) == 1

    def test_find_sccs_complete_scc(self, scc_finder):
        """Test finding SCCs with all vertices in one component."""
        edges = [(0, 1), (1, 2), (2, 0), (0, 2), (1, 0), (2, 1)]
        sccs = scc_finder.find_sccs(edges)
        assert len(sccs) == 1
        assert set(sccs[0]) == {0, 1, 2}

    def test_find_sccs_chain(self, scc_finder):
        """Test finding SCCs with chain (no cycles)."""
        edges = [(0, 1), (1, 2), (2, 3)]
        sccs = scc_finder.find_sccs(edges)
        assert len(sccs) == 4
        for scc in sccs:
            assert len(scc) == 1

    def test_find_sccs_complex_graph(self, scc_finder):
        """Test finding SCCs with complex graph."""
        edges = [
            (0, 1),
            (1, 2),
            (2, 0),
            (3, 4),
            (4, 3),
            (5, 6),
            (6, 5),
            (7, 8),
        ]
        sccs = scc_finder.find_sccs(edges, num_vertices=9)
        assert len(sccs) >= 3
        scc_sets = [set(scc) for scc in sccs]
        assert {0, 1, 2} in scc_sets
        assert {3, 4} in scc_sets
        assert {5, 6} in scc_sets

    def test_get_scc_count_simple(self, scc_finder):
        """Test getting SCC count."""
        edges = [(0, 1), (1, 0), (2, 3), (3, 2)]
        count = scc_finder.get_scc_count(edges)
        assert count == 2

    def test_get_scc_count_empty(self, scc_finder):
        """Test getting SCC count for empty graph."""
        count = scc_finder.get_scc_count([], num_vertices=0)
        assert count == 0

    def test_get_scc_count_isolated(self, scc_finder):
        """Test getting SCC count with isolated vertices."""
        count = scc_finder.get_scc_count([], num_vertices=5)
        assert count == 5

    def test_get_largest_scc_simple(self, scc_finder):
        """Test getting largest SCC."""
        edges = [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5), (5, 4), (6, 7), (7, 6), (8, 9), (9, 8), (10, 11), (11, 10), (12, 13), (13, 12), (14, 15), (15, 14)]
        largest = scc_finder.get_largest_scc(edges, num_vertices=16)
        assert largest is not None
        assert len(largest) == 2

    def test_get_largest_scc_empty(self, scc_finder):
        """Test getting largest SCC for empty graph."""
        largest = scc_finder.get_largest_scc([], num_vertices=0)
        assert largest is None

    def test_get_largest_scc_single(self, scc_finder):
        """Test getting largest SCC with single vertex."""
        largest = scc_finder.get_largest_scc([], num_vertices=1)
        assert largest == [0]

    def test_get_scc_statistics_simple(self, scc_finder):
        """Test getting SCC statistics."""
        edges = [(0, 1), (1, 0), (2, 3), (3, 2), (4, 5), (5, 4)]
        stats = scc_finder.get_scc_statistics(edges, num_vertices=7)
        assert stats["count"] == 4
        assert stats["largest_size"] == 2
        assert stats["smallest_size"] == 1
        assert 2 in stats["sizes"]
        assert 1 in stats["sizes"]

    def test_get_scc_statistics_empty(self, scc_finder):
        """Test getting SCC statistics for empty graph."""
        stats = scc_finder.get_scc_statistics([], num_vertices=0)
        assert stats["count"] == 0
        assert stats["largest_size"] == 0
        assert stats["smallest_size"] == 0
        assert stats["average_size"] == 0.0

    def test_get_scc_statistics_isolated(self, scc_finder):
        """Test getting SCC statistics with isolated vertices."""
        stats = scc_finder.get_scc_statistics([], num_vertices=5)
        assert stats["count"] == 5
        assert stats["largest_size"] == 1
        assert stats["smallest_size"] == 1
        assert stats["average_size"] == 1.0

    def test_compare_performance_simple(self, scc_finder):
        """Test performance comparison."""
        edges = [(0, 1), (1, 2), (2, 0)]
        performance = scc_finder.compare_performance(edges)
        assert performance["num_vertices"] == 3
        assert performance["num_edges"] == 3
        assert performance["find_sccs"]["success"] is True
        assert performance["get_scc_count"]["success"] is True
        assert performance["get_largest_scc"]["success"] is True
        assert performance["get_scc_statistics"]["success"] is True

    def test_compare_performance_with_iterations(self, scc_finder):
        """Test performance comparison with multiple iterations."""
        edges = [(0, 1), (1, 2), (2, 0)]
        performance = scc_finder.compare_performance(edges, iterations=10)
        assert performance["iterations"] == 10
        assert performance["find_sccs"]["success"] is True

    def test_generate_report_success(self, scc_finder, temp_dir):
        """Test report generation."""
        edges = [(0, 1), (1, 2), (2, 0)]
        performance = scc_finder.compare_performance(edges)
        report_path = temp_dir / "report.txt"

        report = scc_finder.generate_report(performance, output_path=str(report_path))

        assert "STRONGLY CONNECTED" in report
        assert "find_sccs" in report
        assert "get_scc_count" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, scc_finder):
        """Test report generation without saving to file."""
        edges = [(0, 1), (1, 2), (2, 0)]
        performance = scc_finder.compare_performance(edges)
        report = scc_finder.generate_report(performance)

        assert "STRONGLY CONNECTED" in report
        assert "find_sccs" in report
        assert "get_scc_count" in report

    def test_find_sccs_large_graph(self, scc_finder):
        """Test finding SCCs with larger graph."""
        edges = [(i, (i + 1) % 10) for i in range(10)]
        sccs = scc_finder.find_sccs(edges, num_vertices=10)
        assert len(sccs) == 1
        assert len(sccs[0]) == 10

    def test_find_sccs_self_loop(self, scc_finder):
        """Test finding SCCs with self-loop."""
        edges = [(0, 0)]
        sccs = scc_finder.find_sccs(edges)
        assert len(sccs) == 1
        assert sccs[0] == [0]

    def test_find_sccs_mixed(self, scc_finder):
        """Test finding SCCs with mixed structure."""
        edges = [
            (0, 1),
            (1, 0),
            (2, 3),
            (3, 4),
            (4, 2),
            (5, 6),
            (6, 5),
        ]
        sccs = scc_finder.find_sccs(edges, num_vertices=7)
        assert len(sccs) >= 3
        scc_sets = [set(scc) for scc in sccs]
        assert {0, 1} in scc_sets
        assert {2, 3, 4} in scc_sets
        assert {5, 6} in scc_sets
