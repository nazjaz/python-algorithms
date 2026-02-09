"""Unit tests for array sum calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import ArraySumCalculator


class TestArraySumCalculator:
    """Test cases for ArraySumCalculator class."""

    @pytest.fixture
    def temp_dir(self):
        """Create temporary directory for testing."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def config_file(self, temp_dir):
        """Create temporary config file."""
        config = {
            "recursion": {"max_depth": 1000},
            "logging": {"level": "INFO", "file": str(temp_dir / "app.log")},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)
        return str(config_path)

    @pytest.fixture
    def calculator(self, config_file):
        """Create ArraySumCalculator instance."""
        return ArraySumCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "recursion": {"max_depth": 500},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calc = ArraySumCalculator(config_path=str(config_path))
        assert calc.config["recursion"]["max_depth"] == 500

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            ArraySumCalculator(config_path="nonexistent.yaml")

    def test_sum_iterative_empty(self, calculator):
        """Test iterative sum with empty array."""
        result = calculator.sum_iterative([])
        assert result == 0.0

    def test_sum_iterative_single_element(self, calculator):
        """Test iterative sum with single element."""
        result = calculator.sum_iterative([5])
        assert result == 5.0

    def test_sum_iterative_multiple_elements(self, calculator):
        """Test iterative sum with multiple elements."""
        result = calculator.sum_iterative([1, 2, 3, 4, 5])
        assert result == 15.0

    def test_sum_iterative_negative_numbers(self, calculator):
        """Test iterative sum with negative numbers."""
        result = calculator.sum_iterative([-5, 3, -1, 0, 2])
        assert result == -1.0

    def test_sum_iterative_floats(self, calculator):
        """Test iterative sum with floating point numbers."""
        result = calculator.sum_iterative([1.5, 2.5, 3.0])
        assert result == 7.0

    def test_sum_recursive_empty(self, calculator):
        """Test recursive sum with empty array."""
        result = calculator.sum_recursive([])
        assert result == 0.0

    def test_sum_recursive_single_element(self, calculator):
        """Test recursive sum with single element."""
        result = calculator.sum_recursive([5])
        assert result == 5.0

    def test_sum_recursive_multiple_elements(self, calculator):
        """Test recursive sum with multiple elements."""
        result = calculator.sum_recursive([1, 2, 3, 4, 5])
        assert result == 15.0

    def test_sum_recursive_negative_numbers(self, calculator):
        """Test recursive sum with negative numbers."""
        result = calculator.sum_recursive([-5, 3, -1, 0, 2])
        assert result == -1.0

    def test_sum_recursive_indexed_empty(self, calculator):
        """Test recursive indexed sum with empty array."""
        result = calculator.sum_recursive_indexed([])
        assert result == 0.0

    def test_sum_recursive_indexed_single_element(self, calculator):
        """Test recursive indexed sum with single element."""
        result = calculator.sum_recursive_indexed([5])
        assert result == 5.0

    def test_sum_recursive_indexed_multiple_elements(self, calculator):
        """Test recursive indexed sum with multiple elements."""
        result = calculator.sum_recursive_indexed([1, 2, 3, 4, 5])
        assert result == 15.0

    def test_all_methods_same_result(self, calculator):
        """Test that all methods produce same result."""
        array = [1, 2, 3, 4, 5]
        iterative = calculator.sum_iterative(array)
        recursive = calculator.sum_recursive(array)
        recursive_idx = calculator.sum_recursive_indexed(array)

        assert iterative == recursive == recursive_idx

    def test_compare_performance(self, calculator):
        """Test performance comparison."""
        comparison = calculator.compare_performance([1, 2, 3, 4, 5])

        assert "array_length" in comparison
        assert "iterative" in comparison
        assert "recursive" in comparison
        assert "recursive_indexed" in comparison

        assert comparison["iterative"]["success"] is True
        assert comparison["recursive"]["success"] is True
        assert comparison["recursive_indexed"]["success"] is True

        assert comparison["iterative"]["result"] == comparison["recursive"]["result"]
        assert comparison["recursive"]["result"] == comparison["recursive_indexed"]["result"]

    def test_compare_performance_multiple_iterations(self, calculator):
        """Test performance comparison with multiple iterations."""
        comparison = calculator.compare_performance([1, 2, 3], iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            method.get("success", False)
            for method in [
                comparison["iterative"],
                comparison["recursive"],
                comparison["recursive_indexed"],
            ]
        )

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        comparison = calculator.compare_performance([1, 2, 3, 4, 5])
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "ARRAY SUM CALCULATION PERFORMANCE COMPARISON REPORT" in report
        assert "Iterative Method" in report
        assert "Recursive Method" in report
