"""Unit tests for knapsack problem solver module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import KnapsackSolver


class TestKnapsackSolver:
    """Test cases for KnapsackSolver class."""

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
        """Create KnapsackSolver instance."""
        return KnapsackSolver(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        solver = KnapsackSolver(config_path=str(config_path))
        assert solver.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test configuration loading with missing file."""
        with pytest.raises(FileNotFoundError):
            KnapsackSolver(config_path="nonexistent.yaml")

    def test_validate_inputs_empty_weights(self, solver):
        """Test validation with empty weights."""
        with pytest.raises(ValueError, match="cannot be empty"):
            solver._validate_inputs([], [1, 2], 10)

    def test_validate_inputs_empty_values(self, solver):
        """Test validation with empty values."""
        with pytest.raises(ValueError, match="cannot be empty"):
            solver._validate_inputs([1, 2], [], 10)

    def test_validate_inputs_mismatched_lengths(self, solver):
        """Test validation with mismatched array lengths."""
        with pytest.raises(ValueError, match="must match"):
            solver._validate_inputs([1, 2], [10], 10)

    def test_validate_inputs_negative_capacity(self, solver):
        """Test validation with negative capacity."""
        with pytest.raises(ValueError, match="must be positive"):
            solver._validate_inputs([1, 2], [10, 20], -5)

    def test_validate_inputs_zero_capacity(self, solver):
        """Test validation with zero capacity."""
        with pytest.raises(ValueError, match="must be positive"):
            solver._validate_inputs([1, 2], [10, 20], 0)

    def test_validate_inputs_zero_weight(self, solver):
        """Test validation with zero weight."""
        with pytest.raises(ValueError, match="weights must be positive"):
            solver._validate_inputs([0, 2], [10, 20], 10)

    def test_validate_inputs_negative_weight(self, solver):
        """Test validation with negative weight."""
        with pytest.raises(ValueError, match="weights must be positive"):
            solver._validate_inputs([-1, 2], [10, 20], 10)

    def test_validate_inputs_negative_value(self, solver):
        """Test validation with negative value."""
        with pytest.raises(ValueError, match="values must be non-negative"):
            solver._validate_inputs([1, 2], [-10, 20], 10)

    def test_validate_inputs_valid(self, solver):
        """Test validation with valid inputs."""
        solver._validate_inputs([1, 2, 3], [10, 20, 30], 10)

    def test_solve_01_knapsack_basic(self, solver):
        """Test basic 0-1 knapsack solution."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 220.0
        assert items == [1, 2]

    def test_solve_01_knapsack_single_item(self, solver):
        """Test 0-1 knapsack with single item."""
        weights = [10]
        values = [60]
        capacity = 10

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 60.0
        assert items == [0]

    def test_solve_01_knapsack_capacity_too_small(self, solver):
        """Test 0-1 knapsack when capacity is smaller than all items."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 5

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 0.0
        assert items == []

    def test_solve_01_knapsack_capacity_large(self, solver):
        """Test 0-1 knapsack when capacity is larger than sum of items."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 100

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 280.0
        assert items == [0, 1, 2]

    def test_solve_01_knapsack_equal_values(self, solver):
        """Test 0-1 knapsack with items of equal value."""
        weights = [10, 20, 30]
        values = [50, 50, 50]
        capacity = 40

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 100.0
        assert len(items) == 2

    def test_solve_fractional_knapsack_basic(self, solver):
        """Test basic fractional knapsack solution."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 240.0
        assert len(items) == 2
        assert items[0][0] == 0
        assert items[0][1] == 1.0
        assert items[1][0] == 2
        assert items[1][1] == 1.0

    def test_solve_fractional_knapsack_partial_item(self, solver):
        """Test fractional knapsack with partial item selection."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 15

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 90.0
        assert len(items) == 1
        assert items[0][0] == 0
        assert items[0][1] == 1.0

    def test_solve_fractional_knapsack_single_item(self, solver):
        """Test fractional knapsack with single item."""
        weights = [10]
        values = [60]
        capacity = 10

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 60.0
        assert items == [(0, 1.0)]

    def test_solve_fractional_knapsack_capacity_too_small(self, solver):
        """Test fractional knapsack when capacity is smaller than all items."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 5

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 30.0
        assert len(items) == 1
        assert items[0][1] == 0.5

    def test_solve_fractional_knapsack_capacity_large(self, solver):
        """Test fractional knapsack when capacity is larger than sum."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 100

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 280.0
        assert len(items) == 3
        assert all(frac == 1.0 for _, frac in items)

    def test_solve_fractional_knapsack_equal_ratios(self, solver):
        """Test fractional knapsack with equal value-to-weight ratios."""
        weights = [10, 20, 30]
        values = [50, 100, 150]
        capacity = 40

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 200.0
        assert sum(w * frac for (i, frac), w in zip(items, weights)) == 40

    def test_compare_approaches_basic(self, solver):
        """Test comparison of both approaches."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        results = solver.compare_approaches(weights, values, capacity)

        assert results["num_items"] == 3
        assert results["capacity"] == 50
        assert results["zero_one"]["success"] is True
        assert results["fractional"]["success"] is True
        assert results["fractional"]["value"] >= results["zero_one"]["value"]
        assert "value_difference" in results

    def test_compare_approaches_fractional_better(self, solver):
        """Test that fractional typically yields higher value."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 25

        results = solver.compare_approaches(weights, values, capacity)

        assert results["fractional"]["value"] >= results["zero_one"]["value"]
        assert results["fractional_better"] is True

    def test_compare_approaches_with_iterations(self, solver):
        """Test comparison with multiple iterations."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        results = solver.compare_approaches(weights, values, capacity, iterations=10)

        assert results["iterations"] == 10
        assert results["zero_one"]["success"] is True
        assert results["fractional"]["success"] is True

    def test_generate_report_success(self, solver, temp_dir):
        """Test report generation."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        comparison = solver.compare_approaches(weights, values, capacity)
        report_path = temp_dir / "report.txt"

        report = solver.generate_report(comparison, output_path=str(report_path))

        assert "KNAPSACK PROBLEM" in report
        assert "0-1 KNAPSACK" in report
        assert "FRACTIONAL KNAPSACK" in report
        assert report_path.exists()

    def test_generate_report_no_output(self, solver):
        """Test report generation without saving to file."""
        weights = [10, 20, 30]
        values = [60, 100, 120]
        capacity = 50

        comparison = solver.compare_approaches(weights, values, capacity)
        report = solver.generate_report(comparison)

        assert "KNAPSACK PROBLEM" in report
        assert "0-1 KNAPSACK" in report
        assert "FRACTIONAL KNAPSACK" in report

    def test_solve_01_knapsack_invalid_inputs(self, solver):
        """Test 0-1 knapsack with invalid inputs."""
        with pytest.raises(ValueError):
            solver.solve_01_knapsack([], [1, 2], 10)

    def test_solve_fractional_knapsack_invalid_inputs(self, solver):
        """Test fractional knapsack with invalid inputs."""
        with pytest.raises(ValueError):
            solver.solve_fractional_knapsack([1, 2], [], 10)

    def test_solve_01_knapsack_zero_value_item(self, solver):
        """Test 0-1 knapsack with item having zero value."""
        weights = [10, 20]
        values = [0, 100]
        capacity = 30

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value == 100.0
        assert items == [1]

    def test_solve_fractional_knapsack_zero_value_item(self, solver):
        """Test fractional knapsack with item having zero value."""
        weights = [10, 20]
        values = [0, 100]
        capacity = 30

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value == 100.0
        assert items == [(1, 1.0)]

    def test_solve_01_knapsack_large_problem(self, solver):
        """Test 0-1 knapsack with larger problem."""
        weights = [1, 3, 4, 5, 2, 6, 7, 8, 9, 10]
        values = [1, 4, 5, 7, 2, 8, 9, 10, 11, 12]
        capacity = 20

        value, items = solver.solve_01_knapsack(weights, values, capacity)

        assert value > 0
        assert len(items) > 0
        total_weight = sum(weights[i] for i in items)
        assert total_weight <= capacity

    def test_solve_fractional_knapsack_large_problem(self, solver):
        """Test fractional knapsack with larger problem."""
        weights = [1, 3, 4, 5, 2, 6, 7, 8, 9, 10]
        values = [1, 4, 5, 7, 2, 8, 9, 10, 11, 12]
        capacity = 20

        value, items = solver.solve_fractional_knapsack(weights, values, capacity)

        assert value > 0
        assert len(items) > 0
        total_weight = sum(weights[i] * frac for i, frac in items)
        assert total_weight <= capacity + 0.001
