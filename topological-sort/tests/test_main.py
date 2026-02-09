"""Unit tests for topological sort module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import TopologicalSort


class TestTopologicalSort:
    """Test cases for TopologicalSort class."""

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
    def solver(self, config_file):
        """Create TopologicalSort instance."""
        return TopologicalSort(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        solver = TopologicalSort(config_path=str(config_path))
        assert solver.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test configuration loading with missing file."""
        with pytest.raises(FileNotFoundError):
            TopologicalSort(config_path="nonexistent.yaml")

    def test_build_graph_empty_edges_no_vertices(self, solver):
        """Test building graph with no edges and no vertices."""
        with pytest.raises(ValueError, match="must be provided"):
            solver._build_graph([], None)

    def test_build_graph_empty_edges_with_vertices(self, solver):
        """Test building graph with no edges but specified vertices."""
        adjacency_list, vertices = solver._build_graph([], num_vertices=5)
        assert len(vertices) == 5
        assert all(v in adjacency_list for v in vertices)

    def test_build_graph_with_edges(self, solver):
        """Test building graph with edges."""
        edges = [(0, 1), (1, 2), (2, 3)]
        adjacency_list, vertices = solver._build_graph(edges)
        assert 0 in adjacency_list
        assert 1 in adjacency_list[0]
        assert len(vertices) == 4

    def test_build_graph_negative_vertex(self, solver):
        """Test building graph with negative vertex index."""
        with pytest.raises(ValueError, match="non-negative"):
            solver._build_graph([(-1, 0)])

    def test_build_graph_num_vertices_too_small(self, solver):
        """Test building graph with num_vertices too small."""
        edges = [(0, 1), (2, 3)]
        with pytest.raises(ValueError, match="less than"):
            solver._build_graph(edges, num_vertices=2)

    def test_calculate_in_degrees(self, solver):
        """Test in-degree calculation."""
        edges = [(0, 1), (0, 2), (1, 2)]
        adjacency_list, vertices = solver._build_graph(edges)
        in_degrees = solver._calculate_in_degrees(adjacency_list, vertices)
        assert in_degrees[0] == 0
        assert in_degrees[1] == 1
        assert in_degrees[2] == 2

    def test_sort_kahn_simple_dag(self, solver):
        """Test Kahn's algorithm with simple DAG."""
        edges = [(0, 1), (1, 2), (2, 3)]
        order, has_cycle = solver.sort_kahn(edges)
        assert not has_cycle
        assert order == [0, 1, 2, 3]

    def test_sort_kahn_empty_graph(self, solver):
        """Test Kahn's algorithm with empty graph."""
        order, has_cycle = solver.sort_kahn([], num_vertices=0)
        assert not has_cycle
        assert order == []

    def test_sort_kahn_single_vertex(self, solver):
        """Test Kahn's algorithm with single vertex."""
        order, has_cycle = solver.sort_kahn([], num_vertices=1)
        assert not has_cycle
        assert order == [0]

    def test_sort_kahn_cycle_detection(self, solver):
        """Test Kahn's algorithm detects cycle."""
        edges = [(0, 1), (1, 2), (2, 0)]
        order, has_cycle = solver.sort_kahn(edges)
        assert has_cycle
        assert order is None

    def test_sort_kahn_isolated_vertices(self, solver):
        """Test Kahn's algorithm with isolated vertices."""
        edges = [(0, 1)]
        order, has_cycle = solver.sort_kahn(edges, num_vertices=5)
        assert not has_cycle
        assert len(order) == 5
        assert 0 in order
        assert 1 in order

    def test_sort_kahn_multiple_sources(self, solver):
        """Test Kahn's algorithm with multiple source vertices."""
        edges = [(0, 2), (1, 2), (2, 3)]
        order, has_cycle = solver.sort_kahn(edges)
        assert not has_cycle
        assert order.index(0) < order.index(2)
        assert order.index(1) < order.index(2)
        assert order.index(2) < order.index(3)

    def test_sort_dfs_simple_dag(self, solver):
        """Test DFS algorithm with simple DAG."""
        edges = [(0, 1), (1, 2), (2, 3)]
        order, has_cycle = solver.sort_dfs(edges)
        assert not has_cycle
        assert len(order) == 4
        assert order.index(0) < order.index(1)
        assert order.index(1) < order.index(2)
        assert order.index(2) < order.index(3)

    def test_sort_dfs_empty_graph(self, solver):
        """Test DFS algorithm with empty graph."""
        order, has_cycle = solver.sort_dfs([], num_vertices=0)
        assert not has_cycle
        assert order == []

    def test_sort_dfs_single_vertex(self, solver):
        """Test DFS algorithm with single vertex."""
        order, has_cycle = solver.sort_dfs([], num_vertices=1)
        assert not has_cycle
        assert order == [0]

    def test_sort_dfs_cycle_detection(self, solver):
        """Test DFS algorithm detects cycle."""
        edges = [(0, 1), (1, 2), (2, 0)]
        order, has_cycle = solver.sort_dfs(edges)
        assert has_cycle
        assert order is None

    def test_sort_dfs_isolated_vertices(self, solver):
        """Test DFS algorithm with isolated vertices."""
        edges = [(0, 1)]
        order, has_cycle = solver.sort_dfs(edges, num_vertices=5)
        assert not has_cycle
        assert len(order) == 5
        assert 0 in order
        assert 1 in order

    def test_sort_dfs_multiple_sources(self, solver):
        """Test DFS algorithm with multiple source vertices."""
        edges = [(0, 2), (1, 2), (2, 3)]
        order, has_cycle = solver.sort_dfs(edges)
        assert not has_cycle
        assert order.index(0) < order.index(2)
        assert order.index(1) < order.index(2)
        assert order.index(2) < order.index(3)

    def test_detect_cycle_no_cycle(self, solver):
        """Test cycle detection with no cycle."""
        edges = [(0, 1), (1, 2), (2, 3)]
        has_cycle, cycle_path = solver.detect_cycle(edges)
        assert not has_cycle
        assert cycle_path is None

    def test_detect_cycle_simple_cycle(self, solver):
        """Test cycle detection with simple cycle."""
        edges = [(0, 1), (1, 2), (2, 0)]
        has_cycle, cycle_path = solver.detect_cycle(edges)
        assert has_cycle
        assert cycle_path is not None
        assert len(cycle_path) >= 3

    def test_detect_cycle_self_loop(self, solver):
        """Test cycle detection with self-loop."""
        edges = [(0, 0)]
        has_cycle, cycle_path = solver.detect_cycle(edges)
        assert has_cycle
        assert cycle_path is not None

    def test_detect_cycle_multiple_cycles(self, solver):
        """Test cycle detection with multiple cycles."""
        edges = [(0, 1), (1, 0), (2, 3), (3, 2)]
        has_cycle, cycle_path = solver.detect_cycle(edges)
        assert has_cycle
        assert cycle_path is not None

    def test_detect_cycle_empty_graph(self, solver):
        """Test cycle detection with empty graph."""
        has_cycle, cycle_path = solver.detect_cycle([], num_vertices=0)
        assert not has_cycle
        assert cycle_path is None

    def test_compare_approaches_simple_dag(self, solver):
        """Test comparison with simple DAG."""
        edges = [(0, 1), (1, 2), (2, 3)]
        results = solver.compare_approaches(edges)
        assert results["num_vertices"] == 4
        assert results["num_edges"] == 3
        assert results["kahn"]["success"] is True
        assert results["dfs"]["success"] is True
        assert not results["kahn"]["has_cycle"]
        assert not results["dfs"]["has_cycle"]

    def test_compare_approaches_cycle(self, solver):
        """Test comparison with cyclic graph."""
        edges = [(0, 1), (1, 2), (2, 0)]
        results = solver.compare_approaches(edges)
        assert results["kahn"]["success"] is True
        assert results["dfs"]["success"] is True
        assert results["kahn"]["has_cycle"]
        assert results["dfs"]["has_cycle"]

    def test_compare_approaches_with_iterations(self, solver):
        """Test comparison with multiple iterations."""
        edges = [(0, 1), (1, 2), (2, 3)]
        results = solver.compare_approaches(edges, iterations=10)
        assert results["iterations"] == 10
        assert results["kahn"]["success"] is True
        assert results["dfs"]["success"] is True

    def test_compare_approaches_cycle_detection(self, solver):
        """Test comparison includes cycle detection."""
        edges = [(0, 1), (1, 2), (2, 0)]
        results = solver.compare_approaches(edges)
        assert "cycle_detection" in results
        assert results["cycle_detection"]["success"] is True
        assert results["cycle_detection"]["has_cycle"] is True

    def test_generate_report_success(self, solver, temp_dir):
        """Test report generation."""
        edges = [(0, 1), (1, 2), (2, 3)]
        comparison = solver.compare_approaches(edges)
        report_path = temp_dir / "report.txt"

        report = solver.generate_report(comparison, output_path=str(report_path))

        assert "TOPOLOGICAL SORT" in report
        assert "KAHN'S ALGORITHM" in report
        assert "DFS-BASED ALGORITHM" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, solver):
        """Test report generation without saving to file."""
        edges = [(0, 1), (1, 2), (2, 3)]
        comparison = solver.compare_approaches(edges)
        report = solver.generate_report(comparison)

        assert "TOPOLOGICAL SORT" in report
        assert "KAHN'S ALGORITHM" in report
        assert "DFS-BASED ALGORITHM" in report

    def test_sort_kahn_complex_dag(self, solver):
        """Test Kahn's algorithm with complex DAG."""
        edges = [
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
        ]
        order, has_cycle = solver.sort_kahn(edges)
        assert not has_cycle
        assert len(order) == 6
        assert order.index(0) < order.index(3)
        assert order.index(3) < order.index(4)

    def test_sort_dfs_complex_dag(self, solver):
        """Test DFS algorithm with complex DAG."""
        edges = [
            (0, 1),
            (0, 2),
            (1, 3),
            (2, 3),
            (3, 4),
            (4, 5),
        ]
        order, has_cycle = solver.sort_dfs(edges)
        assert not has_cycle
        assert len(order) == 6
        assert order.index(0) < order.index(3)
        assert order.index(3) < order.index(4)

    def test_detect_cycle_complex_cycle(self, solver):
        """Test cycle detection with complex cycle."""
        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 1),
        ]
        has_cycle, cycle_path = solver.detect_cycle(edges)
        assert has_cycle
        assert cycle_path is not None

    def test_sort_kahn_large_graph(self, solver):
        """Test Kahn's algorithm with larger graph."""
        edges = [(i, i + 1) for i in range(20)]
        order, has_cycle = solver.sort_kahn(edges)
        assert not has_cycle
        assert len(order) == 21
        for i in range(20):
            assert order.index(i) < order.index(i + 1)

    def test_sort_dfs_large_graph(self, solver):
        """Test DFS algorithm with larger graph."""
        edges = [(i, i + 1) for i in range(20)]
        order, has_cycle = solver.sort_dfs(edges)
        assert not has_cycle
        assert len(order) == 21
        for i in range(20):
            assert order.index(i) < order.index(i + 1)
