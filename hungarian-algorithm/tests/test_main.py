"""Unit tests for Hungarian algorithm module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import BipartiteGraph, HungarianAlgorithm


class TestHungarianAlgorithm:
    """Test cases for HungarianAlgorithm class."""

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
    def simple_matrix(self, config_file):
        """Create simple cost matrix."""
        return HungarianAlgorithm([[1, 2], [2, 1]], config_path=config_file)

    @pytest.fixture
    def complex_matrix(self, config_file):
        """Create complex cost matrix."""
        matrix = [
            [9, 2, 7, 8],
            [6, 4, 3, 7],
            [5, 8, 1, 8],
            [7, 6, 9, 4],
        ]
        return HungarianAlgorithm(matrix, config_path=config_file)

    def test_hungarian_algorithm_creation(self, config_file):
        """Test HungarianAlgorithm creation."""
        matrix = [[1, 2], [2, 1]]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        assert algorithm.n == 2
        assert len(algorithm.original_matrix) == 2

    def test_hungarian_algorithm_empty_matrix(self):
        """Test creation with empty matrix."""
        with pytest.raises(ValueError):
            HungarianAlgorithm([])

    def test_hungarian_algorithm_non_square(self):
        """Test creation with non-square matrix."""
        with pytest.raises(ValueError):
            HungarianAlgorithm([[1, 2, 3], [4, 5]])

    def test_solve_simple(self, simple_matrix):
        """Test solving simple assignment problem."""
        min_cost, assignments = simple_matrix.solve()
        assert min_cost == 2
        assert len(assignments) == 2
        assert simple_matrix.is_valid_assignment(assignments)

    def test_solve_complex(self, complex_matrix):
        """Test solving complex assignment problem."""
        min_cost, assignments = complex_matrix.solve()
        assert min_cost == 13
        assert len(assignments) == 4
        assert complex_matrix.is_valid_assignment(assignments)

    def test_solve_all_zeros(self, config_file):
        """Test solving with all zero costs."""
        matrix = [[0, 0], [0, 0]]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        min_cost, assignments = algorithm.solve()
        assert min_cost == 0
        assert len(assignments) == 2

    def test_solve_identity(self, config_file):
        """Test solving with identity-like matrix."""
        matrix = [[1, 0], [0, 1]]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        min_cost, assignments = algorithm.solve()
        assert min_cost == 2
        assert assignments == [(0, 1), (1, 0)]

    def test_get_assignment_cost(self, simple_matrix):
        """Test getting assignment cost."""
        cost = simple_matrix.get_assignment_cost(0, 0)
        assert cost == 1

        cost = simple_matrix.get_assignment_cost(0, 1)
        assert cost == 2

    def test_get_assignment_cost_invalid(self, simple_matrix):
        """Test getting assignment cost with invalid indices."""
        with pytest.raises(ValueError):
            simple_matrix.get_assignment_cost(-1, 0)
        with pytest.raises(ValueError):
            simple_matrix.get_assignment_cost(0, 10)

    def test_solve_maximization(self, complex_matrix):
        """Test solving maximization problem."""
        max_value, assignments = complex_matrix.solve_maximization()
        assert max_value > 0
        assert len(assignments) == 4
        assert complex_matrix.is_valid_assignment(assignments)

    def test_is_valid_assignment(self, simple_matrix):
        """Test assignment validation."""
        valid = [(0, 0), (1, 1)]
        assert simple_matrix.is_valid_assignment(valid)

        invalid = [(0, 0), (0, 1)]
        assert not simple_matrix.is_valid_assignment(invalid)

        incomplete = [(0, 0)]
        assert not simple_matrix.is_valid_assignment(incomplete)

    def test_large_matrix(self, config_file):
        """Test with larger matrix."""
        matrix = [[i + j for j in range(5)] for i in range(5)]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        min_cost, assignments = algorithm.solve()
        assert min_cost >= 0
        assert len(assignments) == 5
        assert algorithm.is_valid_assignment(assignments)

    def test_same_costs(self, config_file):
        """Test with all same costs."""
        matrix = [[5, 5], [5, 5]]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        min_cost, assignments = algorithm.solve()
        assert min_cost == 10
        assert len(assignments) == 2

    def test_optimal_solution(self, config_file):
        """Test optimal solution correctness."""
        matrix = [
            [250, 400, 350],
            [400, 600, 350],
            [200, 400, 250],
        ]
        algorithm = HungarianAlgorithm(matrix, config_path=config_file)
        min_cost, assignments = algorithm.solve()
        assert min_cost == 850
        assert algorithm.is_valid_assignment(assignments)


class TestBipartiteGraph:
    """Test cases for BipartiteGraph class."""

    def test_bipartite_graph_creation(self):
        """Test BipartiteGraph creation."""
        graph = BipartiteGraph(3, 4)
        assert graph.left_size == 3
        assert graph.right_size == 4
        assert len(graph.edges) == 0

    def test_bipartite_graph_invalid_size(self):
        """Test creation with invalid size."""
        with pytest.raises(ValueError):
            BipartiteGraph(0, 5)
        with pytest.raises(ValueError):
            BipartiteGraph(5, 0)

    def test_add_edge(self):
        """Test adding edge to graph."""
        graph = BipartiteGraph(3, 4)
        graph.add_edge(0, 1, 10)
        assert (0, 1) in graph.edges
        assert graph.edges[(0, 1)] == 10

    def test_add_edge_invalid_vertices(self):
        """Test adding edge with invalid vertices."""
        graph = BipartiteGraph(3, 4)
        with pytest.raises(ValueError):
            graph.add_edge(-1, 1, 10)
        with pytest.raises(ValueError):
            graph.add_edge(0, 10, 10)

    def test_to_cost_matrix(self):
        """Test converting graph to cost matrix."""
        graph = BipartiteGraph(2, 2)
        graph.add_edge(0, 0, 1)
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 0, 2)
        graph.add_edge(1, 1, 1)

        matrix = graph.to_cost_matrix()
        assert len(matrix) == 2
        assert len(matrix[0]) == 2
        assert matrix[0][0] == 1
        assert matrix[0][1] == 2

    def test_solve_assignment(self):
        """Test solving assignment from graph."""
        graph = BipartiteGraph(3, 3)
        graph.add_edge(0, 0, 1)
        graph.add_edge(0, 1, 2)
        graph.add_edge(0, 2, 3)
        graph.add_edge(1, 0, 2)
        graph.add_edge(1, 1, 1)
        graph.add_edge(1, 2, 2)
        graph.add_edge(2, 0, 3)
        graph.add_edge(2, 1, 2)
        graph.add_edge(2, 2, 1)

        min_cost, assignments = graph.solve_assignment()
        assert min_cost >= 0
        assert len(assignments) == 3

    def test_unequal_sizes(self):
        """Test graph with unequal partition sizes."""
        graph = BipartiteGraph(2, 3)
        graph.add_edge(0, 0, 1)
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 1, 1)
        graph.add_edge(1, 2, 2)

        matrix = graph.to_cost_matrix()
        assert len(matrix) == 3
        assert len(matrix[0]) == 3

    def test_sparse_graph(self):
        """Test sparse graph."""
        graph = BipartiteGraph(4, 4)
        graph.add_edge(0, 1, 5)
        graph.add_edge(1, 0, 3)
        graph.add_edge(2, 2, 2)
        graph.add_edge(3, 3, 1)

        min_cost, assignments = graph.solve_assignment()
        assert min_cost >= 0
        assert len(assignments) == 4
