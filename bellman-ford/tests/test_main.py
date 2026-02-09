"""Unit tests for Bellman-Ford algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BellmanFord


class TestBellmanFord:
    """Test cases for BellmanFord class."""

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
    def bf(self, config_file):
        """Create BellmanFord instance."""
        return BellmanFord(config_path=config_file)

    def test_find_shortest_paths_simple(self, bf):
        """Test finding shortest paths for simple graph."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
        assert dist[0] == 0.0
        assert dist[3] == 6.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_empty_graph(self, bf):
        """Test finding shortest paths for empty graph."""
        dist, parent, has_negative_cycle = bf.find_shortest_paths(0, [], 0)
        assert dist == []
        assert parent == []
        assert has_negative_cycle is False

    def test_find_shortest_paths_single_vertex(self, bf):
        """Test finding shortest paths for single vertex."""
        dist, parent, has_negative_cycle = bf.find_shortest_paths(1, [], 0)
        assert dist[0] == 0.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_disconnected(self, bf):
        """Test finding shortest paths for disconnected graph."""
        edges = [(0, 1, 1), (2, 3, 2)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
        assert dist[3] == float("inf")
        assert has_negative_cycle is False

    def test_find_shortest_paths_negative_weights(self, bf):
        """Test finding shortest paths with negative weights."""
        edges = [(0, 1, -1), (1, 2, 2), (2, 3, 3)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
        assert dist[3] == 4.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_negative_cycle(self, bf):
        """Test finding shortest paths with negative cycle."""
        edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(3, edges, 0)
        assert has_negative_cycle is True

    def test_find_shortest_paths_invalid_source(self, bf):
        """Test finding shortest paths with invalid source."""
        with pytest.raises(ValueError, match="out of range"):
            bf.find_shortest_paths(4, [], 10)

    def test_find_shortest_paths_negative_num_vertices(self, bf):
        """Test finding shortest paths with negative number of vertices."""
        with pytest.raises(ValueError, match="non-negative"):
            bf.find_shortest_paths(-1, [], 0)

    def test_find_negative_cycle_no_cycle(self, bf):
        """Test finding negative cycle when no cycle exists."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        cycle = bf.find_negative_cycle(4, edges, 0)
        assert cycle is None

    def test_find_negative_cycle_with_cycle(self, bf):
        """Test finding negative cycle when cycle exists."""
        edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
        cycle = bf.find_negative_cycle(3, edges, 0)
        assert cycle is not None
        assert len(cycle) > 0

    def test_reconstruct_path_simple(self, bf):
        """Test path reconstruction for simple path."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, parent, _ = bf.find_shortest_paths(4, edges, 0)
        path = bf.reconstruct_path(parent, 0, 3)
        assert path == [0, 1, 2, 3]

    def test_reconstruct_path_direct(self, bf):
        """Test path reconstruction for direct edge."""
        edges = [(0, 1, 1)]
        dist, parent, _ = bf.find_shortest_paths(2, edges, 0)
        path = bf.reconstruct_path(parent, 0, 1)
        assert path == [0, 1]

    def test_reconstruct_path_no_path(self, bf):
        """Test path reconstruction when no path exists."""
        edges = [(0, 1, 1), (2, 3, 2)]
        dist, parent, _ = bf.find_shortest_paths(4, edges, 0)
        path = bf.reconstruct_path(parent, 0, 3)
        assert path is None

    def test_reconstruct_path_same_vertex(self, bf):
        """Test path reconstruction for same vertex."""
        edges = [(0, 1, 1)]
        dist, parent, _ = bf.find_shortest_paths(2, edges, 0)
        path = bf.reconstruct_path(parent, 0, 0)
        assert path == [0]

    def test_get_shortest_distance(self, bf):
        """Test getting shortest distance."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        distance = bf.get_shortest_distance(4, edges, 0, 3)
        assert distance == 6.0

    def test_get_shortest_distance_no_path(self, bf):
        """Test getting shortest distance when no path exists."""
        edges = [(0, 1, 1), (2, 3, 2)]
        distance = bf.get_shortest_distance(4, edges, 0, 3)
        assert distance is None

    def test_get_shortest_distance_negative_cycle(self, bf):
        """Test getting shortest distance with negative cycle."""
        edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
        distance = bf.get_shortest_distance(3, edges, 0, 2)
        assert distance is None

    def test_get_all_distances(self, bf):
        """Test getting all distances."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, has_negative_cycle = bf.get_all_distances(4, edges, 0)
        assert len(dist) == 4
        assert has_negative_cycle is False
        assert dist[0] == 0.0

    def test_compare_performance(self, bf):
        """Test performance comparison."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = bf.compare_performance(4, edges, 0, iterations=1)
        assert performance["num_vertices"] == 4
        assert performance["num_edges"] == 3
        assert performance["source"] == 0
        assert performance["bellman_ford"]["success"] is True

    def test_compare_performance_with_iterations(self, bf):
        """Test performance comparison with multiple iterations."""
        edges = [(0, 1, 1), (1, 2, 2)]
        performance = bf.compare_performance(3, edges, 0, iterations=10)
        assert performance["iterations"] == 10
        assert performance["bellman_ford"]["success"] is True

    def test_generate_report_success(self, bf, temp_dir):
        """Test report generation."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = bf.compare_performance(4, edges, 0)
        report_path = temp_dir / "report.txt"

        report = bf.generate_report(performance, output_path=str(report_path))

        assert "BELLMAN-FORD" in report
        assert "ALGORITHM" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, bf):
        """Test report generation without saving to file."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = bf.compare_performance(4, edges, 0)
        report = bf.generate_report(performance)

        assert "BELLMAN-FORD" in report
        assert "ALGORITHM" in report

    def test_large_graph(self, bf):
        """Test with larger graph."""
        edges = [(i, i + 1, 1) for i in range(9)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(10, edges, 0)
        assert dist[9] == 9.0
        assert has_negative_cycle is False

    def test_negative_weights_no_cycle(self, bf):
        """Test with negative weights but no negative cycle."""
        edges = [(0, 1, -1), (1, 2, 2), (2, 3, 3)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
        assert dist[3] == 4.0
        assert has_negative_cycle is False

    def test_multiple_edges(self, bf):
        """Test with multiple edges between same pair."""
        edges = [(0, 1, 5), (0, 1, 2)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(2, edges, 0)
        assert dist[1] == 2.0
        assert has_negative_cycle is False

    def test_self_loops(self, bf):
        """Test with self-loops."""
        edges = [(0, 0, 1), (0, 1, 2)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(2, edges, 0)
        assert dist[0] == 0.0
        assert has_negative_cycle is False

    def test_negative_self_loop(self, bf):
        """Test with negative self-loop."""
        edges = [(0, 0, -1), (0, 1, 2)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(2, edges, 0)
        assert has_negative_cycle is True

    def test_floating_point_weights(self, bf):
        """Test with floating point weights."""
        edges = [(0, 1, 1.5), (1, 2, 2.5), (2, 3, 3.5)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 0)
        assert abs(dist[3] - 7.5) < 0.001
        assert has_negative_cycle is False

    def test_different_source(self, bf):
        """Test with different source vertex."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, parent, has_negative_cycle = bf.find_shortest_paths(4, edges, 2)
        assert dist[2] == 0.0
        assert dist[3] == 3.0
        assert has_negative_cycle is False

    def test_path_reconstruction_various_paths(self, bf):
        """Test path reconstruction for various paths."""
        edges = [
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (0, 3, 5),
        ]
        dist, parent, _ = bf.find_shortest_paths(4, edges, 0)
        path = bf.reconstruct_path(parent, 0, 3)
        assert path == [0, 1, 2, 3]
        assert dist[3] == 3.0
