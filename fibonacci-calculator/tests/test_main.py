"""Unit tests for fibonacci calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FibonacciCalculator


class TestFibonacciCalculator:
    """Test cases for FibonacciCalculator class."""

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
        """Create FibonacciCalculator instance."""
        return FibonacciCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "recursion": {"max_depth": 500},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calc = FibonacciCalculator(config_path=str(config_path))
        assert calc.config["recursion"]["max_depth"] == 500

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            FibonacciCalculator(config_path="nonexistent.yaml")

    def test_fibonacci_naive_base_cases(self, calculator):
        """Test naive recursion with base cases."""
        assert calculator.fibonacci_naive(0) == 0
        assert calculator.fibonacci_naive(1) == 1

    def test_fibonacci_naive_small_values(self, calculator):
        """Test naive recursion with small values."""
        assert calculator.fibonacci_naive(2) == 1
        assert calculator.fibonacci_naive(3) == 2
        assert calculator.fibonacci_naive(4) == 3
        assert calculator.fibonacci_naive(5) == 5
        assert calculator.fibonacci_naive(6) == 8
        assert calculator.fibonacci_naive(7) == 13

    def test_fibonacci_naive_negative(self, calculator):
        """Test naive recursion with negative input."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculator.fibonacci_naive(-1)

    def test_fibonacci_memoized_base_cases(self, calculator):
        """Test memoized approach with base cases."""
        calculator.memo = {}
        assert calculator.fibonacci_memoized(0) == 0
        assert calculator.fibonacci_memoized(1) == 1

    def test_fibonacci_memoized_small_values(self, calculator):
        """Test memoized approach with small values."""
        calculator.memo = {}
        assert calculator.fibonacci_memoized(2) == 1
        assert calculator.fibonacci_memoized(3) == 2
        assert calculator.fibonacci_memoized(4) == 3
        assert calculator.fibonacci_memoized(5) == 5
        assert calculator.fibonacci_memoized(6) == 8
        assert calculator.fibonacci_memoized(7) == 13

    def test_fibonacci_memoized_cache(self, calculator):
        """Test that memoization cache is used."""
        calculator.memo = {}
        calculator.fibonacci_memoized(5)
        assert 5 in calculator.memo
        assert calculator.memo[5] == 5

    def test_fibonacci_memoized_negative(self, calculator):
        """Test memoized approach with negative input."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculator.fibonacci_memoized(-1)

    def test_fibonacci_iterative_base_cases(self, calculator):
        """Test iterative approach with base cases."""
        assert calculator.fibonacci_iterative(0) == 0
        assert calculator.fibonacci_iterative(1) == 1

    def test_fibonacci_iterative_small_values(self, calculator):
        """Test iterative approach with small values."""
        assert calculator.fibonacci_iterative(2) == 1
        assert calculator.fibonacci_iterative(3) == 2
        assert calculator.fibonacci_iterative(4) == 3
        assert calculator.fibonacci_iterative(5) == 5
        assert calculator.fibonacci_iterative(6) == 8
        assert calculator.fibonacci_iterative(7) == 13

    def test_fibonacci_iterative_negative(self, calculator):
        """Test iterative approach with negative input."""
        with pytest.raises(ValueError, match="must be non-negative"):
            calculator.fibonacci_iterative(-1)

    def test_all_methods_same_result(self, calculator):
        """Test that all methods produce same result."""
        test_cases = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

        for n in test_cases:
            calculator.memo = {}
            calculator.recursive_calls = 0
            naive = calculator.fibonacci_naive(n)

            calculator.memo = {}
            calculator.recursive_calls = 0
            memoized = calculator.fibonacci_memoized(n)

            iterative = calculator.fibonacci_iterative(n)

            assert naive == memoized == iterative, f"Failed for n={n}"

    def test_compare_approaches(self, calculator):
        """Test performance comparison."""
        comparison = calculator.compare_approaches(10)

        assert "n" in comparison
        assert "naive_recursion" in comparison
        assert "memoized" in comparison
        assert "iterative" in comparison

        assert comparison["naive_recursion"]["success"] is True
        assert comparison["memoized"]["success"] is True
        assert comparison["iterative"]["success"] is True

        assert (
            comparison["naive_recursion"]["result"]
            == comparison["memoized"]["result"]
            == comparison["iterative"]["result"]
        )

    def test_compare_approaches_multiple_iterations(self, calculator):
        """Test performance comparison with multiple iterations."""
        comparison = calculator.compare_approaches(10, iterations=10)

        assert comparison["iterations"] == 10
        assert all(
            method.get("success", False)
            for method in [
                comparison["naive_recursion"],
                comparison["memoized"],
                comparison["iterative"],
            ]
        )

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        comparison = calculator.compare_approaches(10)
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "FIBONACCI CALCULATION PERFORMANCE COMPARISON REPORT" in report
        assert "Naive Recursion" in report
        assert "Memoized (Dynamic Programming)" in report
        assert "Iterative" in report

    def test_memoization_reduces_calls(self, calculator):
        """Test that memoization reduces recursive calls."""
        calculator.memo = {}
        calculator.recursive_calls = 0
        calculator.fibonacci_naive(10)
        naive_calls = calculator.recursive_calls

        calculator.memo = {}
        calculator.recursive_calls = 0
        calculator.fibonacci_memoized(10)
        memoized_calls = calculator.recursive_calls

        assert memoized_calls < naive_calls

    def test_larger_values(self, calculator):
        """Test with larger values."""
        n = 20
        calculator.memo = {}
        memoized = calculator.fibonacci_memoized(n)
        iterative = calculator.fibonacci_iterative(n)

        assert memoized == iterative
