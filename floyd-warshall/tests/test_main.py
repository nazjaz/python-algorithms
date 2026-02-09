"""Unit tests for Floyd-Warshall algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FloydWarshall


class TestFloydWarshall:
    """Test cases for FloydWarshall class."""

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
    def fw(self, config_file):
        """Create FloydWarshall instance."""
        return FloydWarshall(config_path=config_file)

    def test_find_shortest_paths_simple(self, fw):
        """Test finding shortest paths for simple graph."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3), (0, 3, 4)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert dist[0][3] == 4.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_empty_graph(self, fw):
        """Test finding shortest paths for empty graph."""
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(0, [])
        assert dist == []
        assert next_matrix == []
        assert has_negative_cycle is False

    def test_find_shortest_paths_single_vertex(self, fw):
        """Test finding shortest paths for single vertex."""
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(1, [])
        assert dist[0][0] == 0.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_disconnected(self, fw):
        """Test finding shortest paths for disconnected graph."""
        edges = [(0, 1, 1), (2, 3, 2)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert dist[0][3] == float("inf")
        assert has_negative_cycle is False

    def test_find_shortest_paths_negative_weights(self, fw):
        """Test finding shortest paths with negative weights."""
        edges = [(0, 1, -1), (1, 2, 2), (2, 3, 3)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert dist[0][3] == 4.0
        assert has_negative_cycle is False

    def test_find_shortest_paths_negative_cycle(self, fw):
        """Test finding shortest paths with negative cycle."""
        edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(3, edges)
        assert has_negative_cycle is True

    def test_find_shortest_paths_negative_num_vertices(self, fw):
        """Test finding shortest paths with negative number of vertices."""
        with pytest.raises(ValueError, match="non-negative"):
            fw.find_shortest_paths(-1, [])

    def test_reconstruct_path_simple(self, fw):
        """Test path reconstruction for simple path."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, next_matrix, _ = fw.find_shortest_paths(4, edges)
        path = fw.reconstruct_path(next_matrix, 0, 3)
        assert path == [0, 1, 2, 3]

    def test_reconstruct_path_direct(self, fw):
        """Test path reconstruction for direct edge."""
        edges = [(0, 1, 1)]
        dist, next_matrix, _ = fw.find_shortest_paths(2, edges)
        path = fw.reconstruct_path(next_matrix, 0, 1)
        assert path == [0, 1]

    def test_reconstruct_path_no_path(self, fw):
        """Test path reconstruction when no path exists."""
        edges = [(0, 1, 1), (2, 3, 2)]
        dist, next_matrix, _ = fw.find_shortest_paths(4, edges)
        path = fw.reconstruct_path(next_matrix, 0, 3)
        assert path is None

    def test_reconstruct_path_same_vertex(self, fw):
        """Test path reconstruction for same vertex."""
        edges = [(0, 1, 1)]
        dist, next_matrix, _ = fw.find_shortest_paths(2, edges)
        path = fw.reconstruct_path(next_matrix, 0, 0)
        assert path == [0]

    def test_get_shortest_distance(self, fw):
        """Test getting shortest distance."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        distance = fw.get_shortest_distance(4, edges, 0, 3)
        assert distance == 6.0

    def test_get_shortest_distance_no_path(self, fw):
        """Test getting shortest distance when no path exists."""
        edges = [(0, 1, 1), (2, 3, 2)]
        distance = fw.get_shortest_distance(4, edges, 0, 3)
        assert distance is None

    def test_get_shortest_distance_negative_cycle(self, fw):
        """Test getting shortest distance with negative cycle."""
        edges = [(0, 1, 1), (1, 2, -2), (2, 0, -1)]
        distance = fw.get_shortest_distance(3, edges, 0, 2)
        assert distance is None

    def test_get_all_distances(self, fw):
        """Test getting all distances."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        dist, has_negative_cycle = fw.get_all_distances(4, edges)
        assert len(dist) == 4
        assert len(dist[0]) == 4
        assert has_negative_cycle is False
        assert dist[0][0] == 0.0

    def test_compare_performance(self, fw):
        """Test performance comparison."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = fw.compare_performance(4, edges, iterations=1)
        assert performance["num_vertices"] == 4
        assert performance["num_edges"] == 3
        assert performance["floyd_warshall"]["success"] is True

    def test_compare_performance_with_iterations(self, fw):
        """Test performance comparison with multiple iterations."""
        edges = [(0, 1, 1), (1, 2, 2)]
        performance = fw.compare_performance(3, edges, iterations=10)
        assert performance["iterations"] == 10
        assert performance["floyd_warshall"]["success"] is True

    def test_generate_report_success(self, fw, temp_dir):
        """Test report generation."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = fw.compare_performance(4, edges)
        report_path = temp_dir / "report.txt"

        report = fw.generate_report(performance, output_path=str(report_path))

        assert "FLOYD-WARSHALL" in report
        assert "ALGORITHM" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, fw):
        """Test report generation without saving to file."""
        edges = [(0, 1, 1), (1, 2, 2), (2, 3, 3)]
        performance = fw.compare_performance(4, edges)
        report = fw.generate_report(performance)

        assert "FLOYD-WARSHALL" in report
        assert "ALGORITHM" in report

    def test_large_graph(self, fw):
        """Test with larger graph."""
        edges = [(i, i + 1, 1) for i in range(9)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(10, edges)
        assert dist[0][9] == 9.0
        assert has_negative_cycle is False

    def test_self_loops(self, fw):
        """Test with self-loops."""
        edges = [(0, 0, 1), (0, 1, 2)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(2, edges)
        assert dist[0][0] == 0.0
        assert has_negative_cycle is False

    def test_multiple_edges(self, fw):
        """Test with multiple edges between same pair."""
        edges = [(0, 1, 5), (0, 1, 2)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(2, edges)
        assert dist[0][1] == 2.0
        assert has_negative_cycle is False

    def test_complete_graph(self, fw):
        """Test with complete graph."""
        edges = [
            (0, 1, 1),
            (0, 2, 2),
            (0, 3, 3),
            (1, 0, 1),
            (1, 2, 1),
            (1, 3, 2),
            (2, 0, 2),
            (2, 1, 1),
            (2, 3, 1),
            (3, 0, 3),
            (3, 1, 2),
            (3, 2, 1),
        ]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert dist[0][3] == 2.0
        assert has_negative_cycle is False

    def test_path_reconstruction_various_paths(self, fw):
        """Test path reconstruction for various paths."""
        edges = [
            (0, 1, 1),
            (1, 2, 1),
            (2, 3, 1),
            (0, 3, 5),
        ]
        dist, next_matrix, _ = fw.find_shortest_paths(4, edges)
        path = fw.reconstruct_path(next_matrix, 0, 3)
        assert path == [0, 1, 2, 3]
        assert dist[0][3] == 3.0

    def test_negative_weights_no_cycle(self, fw):
        """Test with negative weights but no negative cycle."""
        edges = [(0, 1, -1), (1, 2, 2), (2, 3, 3)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert dist[0][3] == 4.0
        assert has_negative_cycle is False

    def test_floating_point_weights(self, fw):
        """Test with floating point weights."""
        edges = [(0, 1, 1.5), (1, 2, 2.5), (2, 3, 3.5)]
        dist, next_matrix, has_negative_cycle = fw.find_shortest_paths(4, edges)
        assert abs(dist[0][3] - 7.5) < 0.001
        assert has_negative_cycle is False
