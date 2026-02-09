"""Unit tests for fast exponentiation calculator module."""

import tempfile
from pathlib import Path

import pytest
import yaml

from src.main import FastExponentiationCalculator


class TestFastExponentiationCalculator:
    """Test cases for FastExponentiationCalculator class."""

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
    def calculator(self, config_file):
        """Create FastExponentiationCalculator instance."""
        return FastExponentiationCalculator(config_path=config_file)

    def test_load_config_success(self, temp_dir):
        """Test successful configuration loading."""
        config = {
            "logging": {"level": "DEBUG"},
        }
        config_path = temp_dir / "config.yaml"
        with open(config_path, "w") as f:
            yaml.dump(config, f)

        calculator = FastExponentiationCalculator(config_path=str(config_path))
        assert calculator.config["logging"]["level"] == "DEBUG"

    def test_load_config_file_not_found(self):
        """Test FileNotFoundError when config file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            FastExponentiationCalculator(config_path="nonexistent.yaml")

    def test_power_naive_simple(self, calculator):
        """Test naive power calculation with simple values."""
        assert calculator.power_naive(2, 3) == 8.0
        assert calculator.power_naive(3, 2) == 9.0
        assert calculator.power_naive(5, 0) == 1.0

    def test_power_naive_zero_exponent(self, calculator):
        """Test naive power with zero exponent."""
        assert calculator.power_naive(10, 0) == 1.0
        assert calculator.power_naive(0, 0) == 1.0

    def test_power_naive_negative_exponent(self, calculator):
        """Test naive power with negative exponent raises error."""
        with pytest.raises(ValueError, match="non-negative"):
            calculator.power_naive(2, -1)

    def test_power_fast_recursive_simple(self, calculator):
        """Test fast recursive power calculation."""
        assert calculator.power_fast_recursive(2, 3) == 8.0
        assert calculator.power_fast_recursive(3, 2) == 9.0
        assert calculator.power_fast_recursive(5, 0) == 1.0

    def test_power_fast_recursive_large_exponent(self, calculator):
        """Test fast recursive with large exponent."""
        result = calculator.power_fast_recursive(2, 10)
        assert result == 1024.0

    def test_power_fast_recursive_negative_exponent(self, calculator):
        """Test fast recursive with negative exponent raises error."""
        with pytest.raises(ValueError, match="non-negative"):
            calculator.power_fast_recursive(2, -1)

    def test_power_fast_iterative_simple(self, calculator):
        """Test fast iterative power calculation."""
        assert calculator.power_fast_iterative(2, 3) == 8.0
        assert calculator.power_fast_iterative(3, 2) == 9.0
        assert calculator.power_fast_iterative(5, 0) == 1.0

    def test_power_fast_iterative_large_exponent(self, calculator):
        """Test fast iterative with large exponent."""
        result = calculator.power_fast_iterative(2, 20)
        assert result == 1048576.0

    def test_power_fast_iterative_negative_exponent(self, calculator):
        """Test fast iterative with negative exponent raises error."""
        with pytest.raises(ValueError, match="non-negative"):
            calculator.power_fast_iterative(2, -1)

    def test_power_fast_recursive_vs_iterative(self, calculator):
        """Test that recursive and iterative give same results."""
        test_cases = [
            (2, 10),
            (3, 5),
            (5, 13),
            (10, 3),
        ]

        for base, exp in test_cases:
            recursive_result = calculator.power_fast_recursive(base, exp)
            iterative_result = calculator.power_fast_iterative(base, exp)
            assert abs(recursive_result - iterative_result) < 1e-10

    def test_power_naive_vs_fast(self, calculator):
        """Test that naive and fast methods give same results."""
        test_cases = [
            (2, 10),
            (3, 5),
            (5, 7),
        ]

        for base, exp in test_cases:
            naive_result = calculator.power_naive(base, exp)
            fast_result = calculator.power_fast_iterative(base, exp)
            assert abs(naive_result - fast_result) < 1e-10

    def test_power_modular_simple(self, calculator):
        """Test modular exponentiation with simple values."""
        result = calculator.power_modular(2, 3, 5)
        assert result == 3  # 2^3 = 8, 8 mod 5 = 3

    def test_power_modular_large(self, calculator):
        """Test modular exponentiation with larger values."""
        result = calculator.power_modular(3, 5, 7)
        assert result == 5  # 3^5 = 243, 243 mod 7 = 5

    def test_power_modular_zero_exponent(self, calculator):
        """Test modular exponentiation with zero exponent."""
        result = calculator.power_modular(10, 0, 7)
        assert result == 1

    def test_power_modular_negative_exponent(self, calculator):
        """Test modular exponentiation with negative exponent raises error."""
        with pytest.raises(ValueError, match="non-negative"):
            calculator.power_modular(2, -1, 5)

    def test_power_modular_invalid_modulus(self, calculator):
        """Test modular exponentiation with invalid modulus raises error."""
        with pytest.raises(ValueError, match="positive"):
            calculator.power_modular(2, 3, 0)
        with pytest.raises(ValueError, match="positive"):
            calculator.power_modular(2, 3, -5)

    def test_calculate_with_analysis_naive(self, calculator):
        """Test calculation with analysis using naive method."""
        analysis = calculator.calculate_with_analysis(2, 10, "naive")
        assert analysis["result"] == 1024.0
        assert analysis["method"] == "naive"
        assert analysis["time_complexity"] == "O(n)"
        assert analysis["expected_operations"] == 10

    def test_calculate_with_analysis_fast(self, calculator):
        """Test calculation with analysis using fast method."""
        analysis = calculator.calculate_with_analysis(2, 10, "fast_iterative")
        assert analysis["result"] == 1024.0
        assert analysis["method"] == "fast_iterative"
        assert analysis["time_complexity"] == "O(log n)"
        assert analysis["expected_operations"] <= 10

    def test_calculate_with_analysis_tracks_steps(self, calculator):
        """Test that analysis tracks steps when requested."""
        analysis = calculator.calculate_with_analysis(
            2, 10, "fast_iterative", track_steps=True
        )
        assert analysis["steps"] is not None
        assert len(analysis["steps"]) > 0

    def test_compare_methods(self, calculator):
        """Test method comparison."""
        comparison = calculator.compare_methods(2, 10)
        assert comparison["naive"]["result"] == comparison["fast"]["result"]
        assert comparison["speedup"] > 1
        assert comparison["results_match"] is True

    def test_compare_methods_large_exponent(self, calculator):
        """Test method comparison with large exponent."""
        comparison = calculator.compare_methods(2, 20)
        assert comparison["results_match"] is True
        assert comparison["speedup"] > 1

    def test_calculate_log_operations(self, calculator):
        """Test log operations calculation."""
        assert calculator._calculate_log_operations(0) == 1
        assert calculator._calculate_log_operations(1) == 1
        assert calculator._calculate_log_operations(2) == 2
        assert calculator._calculate_log_operations(10) <= 4

    def test_generate_report(self, calculator, temp_dir):
        """Test report generation."""
        analysis = calculator.calculate_with_analysis(2, 10, "fast_iterative")
        report_path = temp_dir / "report.txt"
        report = calculator.generate_report(analysis, output_path=str(report_path))

        assert report_path.exists()
        assert "FAST EXPONENTIATION ANALYSIS REPORT" in report
        assert "TIME COMPLEXITY ANALYSIS" in report
        assert "2" in report
        assert "10" in report

    def test_power_fast_recursive_tracks_steps(self, calculator):
        """Test that recursive method tracks steps when requested."""
        calculator.power_fast_recursive(2, 8, track_steps=True)
        assert len(calculator.operation_steps) > 0

    def test_power_fast_iterative_tracks_steps(self, calculator):
        """Test that iterative method tracks steps when requested."""
        calculator.power_fast_iterative(2, 8, track_steps=True)
        assert len(calculator.operation_steps) > 0

    def test_power_modular_tracks_steps(self, calculator):
        """Test that modular method tracks steps when requested."""
        calculator.power_modular(2, 8, 5, track_steps=True)
        assert len(calculator.operation_steps) > 0

    def test_edge_cases_zero_base(self, calculator):
        """Test edge cases with zero base."""
        assert calculator.power_fast_iterative(0, 5) == 0.0
        assert calculator.power_fast_iterative(0, 0) == 1.0

    def test_edge_cases_one_base(self, calculator):
        """Test edge cases with base one."""
        assert calculator.power_fast_iterative(1, 100) == 1.0

    def test_edge_cases_one_exponent(self, calculator):
        """Test edge cases with exponent one."""
        assert calculator.power_fast_iterative(100, 1) == 100.0

    def test_float_base(self, calculator):
        """Test with float base."""
        result = calculator.power_fast_iterative(2.5, 3)
        expected = 2.5 ** 3
        assert abs(result - expected) < 1e-10

    def test_negative_base(self, calculator):
        """Test with negative base."""
        result = calculator.power_fast_iterative(-2, 3)
        assert result == -8.0

        result = calculator.power_fast_iterative(-2, 4)
        assert result == 16.0
