"""Unit tests for factorial calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FactorialCalculator


class TestFactorialCalculator:
    """Test cases for FactorialCalculator class."""

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
        """Create FactorialCalculator instance."""
        return FactorialCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "recursion": {"max_depth": 500},
            "logging": {"level": "INFO"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calc = FactorialCalculator(config_path=str(config_path))
        assert calc.config["recursion"]["max_depth"] == 500

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            FactorialCalculator(config_path="nonexistent.yaml")

    def test_factorial_iterative_zero(self, calculator):
        """Test iterative factorial of 0."""
        result = calculator.factorial_iterative(0)
        assert result == 1

    def test_factorial_iterative_one(self, calculator):
        """Test iterative factorial of 1."""
        result = calculator.factorial_iterative(1)
        assert result == 1

    def test_factorial_iterative_small(self, calculator):
        """Test iterative factorial of small number."""
        result = calculator.factorial_iterative(5)
        assert result == 120

    def test_factorial_iterative_negative(self, calculator):
        """Test ValueError for negative input in iterative."""
        with pytest.raises(ValueError, match="negative"):
            calculator.factorial_iterative(-1)

    def test_factorial_recursive_zero(self, calculator):
        """Test recursive factorial of 0."""
        result = calculator.factorial_recursive(0)
        assert result == 1

    def test_factorial_recursive_one(self, calculator):
        """Test recursive factorial of 1."""
        result = calculator.factorial_recursive(1)
        assert result == 1

    def test_factorial_recursive_small(self, calculator):
        """Test recursive factorial of small number."""
        result = calculator.factorial_recursive(5)
        assert result == 120

    def test_factorial_recursive_negative(self, calculator):
        """Test ValueError for negative input in recursive."""
        with pytest.raises(ValueError, match="negative"):
            calculator.factorial_recursive(-1)

    def test_factorial_memoized_zero(self, calculator):
        """Test memoized factorial of 0."""
        result = calculator.factorial_memoized(0)
        assert result == 1

    def test_factorial_memoized_one(self, calculator):
        """Test memoized factorial of 1."""
        result = calculator.factorial_memoized(1)
        assert result == 1

    def test_factorial_memoized_small(self, calculator):
        """Test memoized factorial of small number."""
        result = calculator.factorial_memoized(5)
        assert result == 120

    def test_factorial_memoized_negative(self, calculator):
        """Test ValueError for negative input in memoized."""
        with pytest.raises(ValueError, match="negative"):
            calculator.factorial_memoized(-1)

    def test_all_methods_same_result(self, calculator):
        """Test that all methods produce same result."""
        n = 10
        iterative = calculator.factorial_iterative(n)
        recursive = calculator.factorial_recursive(n)
        memoized = calculator.factorial_memoized(n)

        assert iterative == recursive == memoized

    def test_compare_performance(self, calculator):
        """Test performance comparison."""
        comparison = calculator.compare_performance(10)

        assert "input" in comparison
        assert "iterative" in comparison
        assert "recursive" in comparison
        assert "memoized" in comparison

        assert comparison["iterative"]["success"] is True
        assert comparison["recursive"]["success"] is True
        assert comparison["memoized"]["success"] is True

        assert comparison["iterative"]["result"] == comparison["recursive"]["result"]
        assert comparison["recursive"]["result"] == comparison["memoized"]["result"]

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        comparison = calculator.compare_performance(5)
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(comparison, output_path=str(report_path))

        assert report_path.exists()
        assert "FACTORIAL CALCULATION PERFORMANCE COMPARISON REPORT" in report
        assert "Iterative" in report
        assert "Recursive" in report
        assert "Memoized" in report
