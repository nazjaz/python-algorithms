"""Unit tests for Kruskal's algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import KruskalMST, UnionFind


class TestUnionFind:
    """Test cases for UnionFind class."""

    def test_init(self):
        """Test UnionFind initialization."""
        uf = UnionFind(5)
        assert len(uf.parent) == 5
        assert len(uf.rank) == 5

    def test_find(self):
        """Test find operation."""
        uf = UnionFind(5)
        assert uf.find(0) == 0
        assert uf.find(4) == 4

    def test_union(self):
        """Test union operation."""
        uf = UnionFind(5)
        result = uf.union(0, 1)
        assert result is True
        assert uf.find(0) == uf.find(1)

    def test_union_already_connected(self):
        """Test union of already connected vertices."""
        uf = UnionFind(5)
        uf.union(0, 1)
        result = uf.union(0, 1)
        assert result is False


class TestKruskalMST:
    """Test cases for KruskalMST class."""

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
    def kruskal(self, config_file):
        """Create KruskalMST instance."""
        return KruskalMST(config_path=config_file)

    def test_find_mst_simple(self, kruskal):
        """Test finding MST for simple graph."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_empty_graph(self, kruskal):
        """Test finding MST for empty graph."""
        mst_edges, total_weight = kruskal.find_mst(0, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_single_vertex(self, kruskal):
        """Test finding MST for single vertex."""
        mst_edges, total_weight = kruskal.find_mst(1, [])
        assert mst_edges == []
        assert total_weight == 0.0

    def test_find_mst_disconnected(self, kruskal):
        """Test finding MST for disconnected graph."""
        edges = [(0, 1, 1), (2, 3, 2)]
        with pytest.raises(ValueError, match="disconnected"):
            kruskal.find_mst(4, edges)

    def test_find_mst_complete_graph(self, kruskal):
        """Test finding MST for complete graph."""
        edges = [
            (0, 1, 1),
            (0, 2, 2),
            (0, 3, 3),
            (1, 2, 4),
            (1, 3, 5),
            (2, 3, 6),
        ]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0

    def test_find_mst_negative_weights(self, kruskal):
        """Test finding MST with negative weights."""
        edges = [(0, 1, -1), (1, 2, -2), (2, 3, -3), (0, 3, -4)]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == -9.0

    def test_find_mst_duplicate_edges(self, kruskal):
        """Test finding MST with duplicate edges."""
        edges = [
            (0, 1, 1),
            (0, 1, 2),
            (1, 2, 3),
            (2, 3, 4),
            (0, 3, 5),
        ]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 8.0

    def test_find_mst_invalid_vertex(self, kruskal):
        """Test finding MST with invalid vertex."""
        edges = [(0, 1, 1), (1, 10, 2)]
        with pytest.raises(ValueError, match="out of range"):
            kruskal.find_mst(4, edges)

    def test_find_mst_self_loop(self, kruskal):
        """Test finding MST with self-loop."""
        edges = [(0, 0, 1), (0, 1, 2)]
        with pytest.raises(ValueError, match="Self-loops"):
            kruskal.find_mst(2, edges)

    def test_get_mst_edges(self, kruskal):
        """Test getting MST edges."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        mst_edges = kruskal.get_mst_edges(4, edges)
        assert len(mst_edges) == 3

    def test_get_mst_weight(self, kruskal):
        """Test getting MST weight."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        total_weight = kruskal.get_mst_weight(4, edges)
        assert total_weight == 6.0

    def test_compare_performance(self, kruskal):
        """Test performance comparison."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        performance = kruskal.compare_performance(4, edges)
        assert performance["num_vertices"] == 4
        assert performance["num_edges"] == 4
        assert performance["find_mst"]["success"] is True
        assert performance["get_mst_edges"]["success"] is True
        assert performance["get_mst_weight"]["success"] is True

    def test_compare_performance_with_iterations(self, kruskal):
        """Test performance comparison with multiple iterations."""
        edges = [(0, 1, 1), (1, 2, 2)]
        performance = kruskal.compare_performance(3, edges, iterations=10)
        assert performance["iterations"] == 10
        assert performance["find_mst"]["success"] is True

    def test_generate_report_success(self, kruskal, temp_dir):
        """Test report generation."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = kruskal.compare_performance(4, edges)
        report_path = temp_dir / "report.txt"

        report = kruskal.generate_report(performance, output_path=str(report_path))

        assert "KRUSKAL" in report
        assert "find_mst" in report
        assert "get_mst_edges" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, kruskal):
        """Test report generation without saving to file."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = kruskal.compare_performance(4, edges)
        report = kruskal.generate_report(performance)

        assert "KRUSKAL" in report
        assert "find_mst" in report
        assert "get_mst_edges" in report

    def test_find_mst_large_graph(self, kruskal):
        """Test finding MST for larger graph."""
        edges = [(i, i + 1, i + 1) for i in range(9)]
        mst_edges, total_weight = kruskal.find_mst(10, edges)
        assert len(mst_edges) == 9
        assert total_weight == sum(range(1, 10))

    def test_find_mst_floating_point_weights(self, kruskal):
        """Test finding MST with floating point weights."""
        edges = [
            (0, 1, 1.5),
            (1, 2, 2.5),
            (2, 3, 3.5),
            (0, 3, 4.5),
        ]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert abs(total_weight - 7.5) < 0.001

    def test_find_mst_optimal_selection(self, kruskal):
        """Test that algorithm selects optimal edges."""
        edges = [
            (0, 1, 1),
            (0, 2, 10),
            (1, 2, 2),
            (1, 3, 3),
            (2, 3, 4),
        ]
        mst_edges, total_weight = kruskal.find_mst(4, edges)
        assert len(mst_edges) == 3
        assert total_weight == 6.0
        edge_weights = [e[2] for e in mst_edges]
        assert 1 in edge_weights
        assert 2 in edge_weights
        assert 3 in edge_weights

    def test_find_mst_negative_num_vertices(self, kruskal):
        """Test finding MST with negative number of vertices."""
        with pytest.raises(ValueError, match="non-negative"):
            kruskal.find_mst(-1, [])
